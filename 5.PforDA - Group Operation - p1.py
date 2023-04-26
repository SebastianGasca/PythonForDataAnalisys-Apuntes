import numpy as np
import pandas as pd

# ---- # ---- # ----
# 1 Data Aggregation and Group Operations
# Aprenderemos 

# 1.Split pandas objects into pieces using one or more keys
# 2.Calculate group summary statistics, like count, mean,  user-defined function
# 3.Apply within-group transformation or other manipulations, like normalization, lm, rank, subset selection
# 4.Compute pivot table and cross-tabulations

#Empecemos por el ejemplo mas sencillo
df = pd.DataFrame({"key1" : ["a", "a", None, "b", "b", "a", None],
                   "key2" : pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
                   "data1" : np.random.standard_normal(7),
                   "data2" : np.random.standard_normal(7)})

#La serie df["data1"] la agrupamos por medio de "key1" y obtenemos la media de los grupos. 
df["data1"].groupby(df["key1"]).mean()
isinstance(df["data1"].groupby(df["key1"]).mean(), pd.Series) #Comprobamos que es una serie

#Podemos hacer grupos por mas de una columna
df["data1"].groupby([df["key1"],df["key2"]]).mean()

#Lo anterior lo hacemos sin considerar que todos esos elementos pertenecen al mismo DF. Si los elementos 
#pertenecen al mismo DF entonces nos sale mas facil. 
#Se aplica el metodo .mean() a todas las columnas agrupadas por "key1" del DF "df" 
df.groupby("key1").mean()

#Si algunas de las columnas no son numericas y aplicamos un .metodo que opera sobre datos numericos
#tenemos que explicitar 
df.groupby("key2").mean(numeric_only = True)

#Agrupamos por mas de una columna
df.groupby(["key1", "key2"]).mean()

#Un metodo util es .size() que nos entrega el tamañano de los grupos
df.groupby("key1").size()

#Otro metodo relacionado a .size() es .count() que nos cuenta los elementos por grupo para cada columna. 
#Omite los NAs
df.groupby("key1").count()




# ---- # ---- # ----
# 1.1 Iterating over Group
# Los objetos agrupados soportan iteracion. La respuesta de un groupby es una tupla compuesta por nombre y 
# los datos del grupo
for name, group in df.groupby("key1"):
    print(name)
    print(group)

# Si se agrupa por mas de una "key" entonces name es una tupla
for (k1,k2), group in df.groupby(["key1","key2"]):
    print((k1,k2))
    print(group)

# Ya que podemos iterar sobre los grupos, podemos generar diccinarios utiles los cuales explorar
pieces = {k1 : group for k1, group in df.groupby("key1")}
pieces["a"]

# Por defecto groupby agrupa por filas, pero lo podemos hacer por columnas
grouped = df.groupby({"key1": "key", "key2": "key", "data1": "data", "data2": "data"}, axis="columns")
for group_key, group_values in grouped:
    print(group_key)
    print(group_values)




# ---- # ---- # ----
# 1.2 Selecting a Column or Subset of Columns
# Podemos seleccionar una sola columna del DF agrupado

df.groupby("key1")["data1"]     #De esta forma tenemos una Serie
df.groupby("key1")[["data2"]]   #De esta forma tenemos un DF

df.groupby(["key1","key2"])[["data2"]].mean()




# ---- # ---- # ----
# 1.3 Grouping with Dictionaries and Series
# No solo usamos array para declarar las variables agrupadas, podemos usar 
# Diccionarios o Series. 

people = pd.DataFrame(np.random.standard_normal((5, 5)),
                      columns=["a", "b", "c", "d", "e"],
                      index=["Joe", "Steve", "Wanda", "Jill", "Trey"])
people.iloc[2:3, [1, 2]] = np.nan 

# Supongamos que queremos una agrupacion por columnas. En estos casos
# es util utilizar un Diccionario como metodo de agrupacion.
mapping = {"a": "red", "b": "red", "c": "blue",
           "d": "blue", "e": "red", "f" : "orange"}

by_column = people.groupby(mapping, axis="columns")

people              #Nuestro DF
by_column.sum()     #Nuestro DF agrupado por columnas

# En vez de usar un Diccionario, podemos usar una Serie. 
map_series = pd.Series(mapping); map_series
people.groupby(map_series, axis="columns").count()




# ---- # ---- # ----
# 1.4 Grouping with Functions
# No solo usamos Arrays, Diccionarios o Series para declarar las variables agrupadas, podemos
# usar funciones de python.

# Las funciones operaran para cada elementos del indice y dado los valores retornados estos seran
# agrupados. Veamos un ejemplo: 

people                          #El DF posee indices con nombres
people.index.str.len()          #Si vemos el largo de cada nombre nos dan valores entre 3 a 5. 

people.groupby(len).mean()      #Si usamos la funcion len para agrupar, los grupos hechos son de 3 a 5

# Podemos mixear el agrupamiento entre funciones y  Arrays, Diccionarios o Series. El siguiente
# Ejemplo muestra un agrupamiento por medio de la funcion .len() en conjunto con un vector

key_list = ["one", "one", "one", "two", "two"]
people.groupby([len, key_list]).min()




# ---- # ---- # ----
# 1.5 Grouping by Index Levels
# Los indices jerarquicos posee niveles, estos pueden ser usados para ser asignados como grupos
columns = pd.MultiIndex.from_arrays([["US", "US", "US", "JP", "JP"],
                                     [1, 3, 5, 1, 3]],
                                     names=["cty", "tenor"])

hier_df = pd.DataFrame(np.random.standard_normal((4, 5)), columns=columns); hier_df

# Agrupamos por medio del nivel "cty", del eje de las columnas
hier_df.groupby(level="cty", axis="columns").count()




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 2 Data Aggregation
# Algunas funciones de agregacion (que producen valores escalares producto de vectores/arrays)
# estan optimizadas para trabajar con DF agrupados. (ver tabla 10.1). 

# any /all ; count ; cummin / cummax ; cumsum ; cumprod ; first / last 
# mean ; median ; min / max ; prod ; quantile ; rank ; size ; sum ; std / var 

# De todas formas podemos usar mas alla de solo esas funciones. 
# Por ejemplo, usamos .nsmallest() que es un metodo para pd.Series que entrega los n valores mas pequeños.
# Este metodo no pertenece a los optimizados de .groupby()

grouped = df.groupby("key1") ; grouped
grouped["data1"].nsmallest(2)

# Si queremos usar nuestra propias funciones de agregacion tenemos el metodo .agg()

def peak_to_peak(arr):
    return arr.max() - arr.min()

grouped.agg(peak_to_peak)

# Tambien funciona el metodo .describe() a pesar de que no es una funcion de agregacion como tal.
grouped.describe()




# ---- # ---- # ----
# 2.1 Column-Wise and Multiple Function Application
#Leeremos un .csv que contiene datos sobre pagos en un restaurant. 

# total_bill (pago)
# tip (propina)

tips = pd.read_csv("tips.csv", sep=None); tips

tips.columns.values
tips.head()
tips.info()

tips.rename(columns={"\ufefftotal_bill":"total_bill"}, inplace=True)

# No se por que no puedo acceder a tips["total_bill"], pero ingrese por su indice
tips["tip_pct"] = tips["tip"] / tips["total_bill"]
tips.head()

# Como vimos antes podemos usar .agg() para ingresar alguna funcion de agregacion
# sobre nuestros grupos. Es posible ingresar mas de una funcion.
grouped = tips.groupby(["day", "smoker"])
grouped_pct = grouped["tip_pct"]

grouped_pct.agg("mean")                             #En vez de usar .mean() usamos .agg("mean")
grouped_pct.agg(["mean","std", peak_to_peak])       #Pasamos una lista de funciones a .agg()

# Podemos asignar nombres a nuestras columnas creadas por las funciones de agregacion
# pasando una tupla. El primer argumento sera el nombre
grouped_pct.agg([("Media","mean"),("Desviacion Estandar","std")])

# Ya sabemos que las funciones de agregacion a un DF se aplican para todas sus columnas, o para un grupo
# seleccionada de ellas. 
functions = ["count", "mean", "max"]
result = grouped[["tip_pct", "total_bill"]].agg(functions); result

# Tambien sabemos que podemos colocar nombres a cada columna creada por las funciones de agregacion
ftuples = [("Average", "mean"), ("Variance", np.var)]
result1 = grouped[["tip_pct", "total_bill"]].agg(ftuples); result1

# Podemos aplicar un funcion de agregacion diferenciada por columnas por medio de diccionarios.
grouped.agg({"tip" : np.max, "size" : "sum"})                           
grouped.agg({"tip_pct" : ["min", "max", "mean", "std"], "size" : "sum"})




# ---- # ---- # ----
# 2.2 Returning Aggregated Data Without Row Indexes
# En todos los ejemplos realizados, los datos agregados vienen con un indice jerarquico 
# compuesto de "unique group key combinations". Ya que esto en ocaciones no es lo mas 
# deseable podemos desactivar este comportamiento por defecto con "as_index = False"

tips.groupby(["day", "smoker"]).mean(numeric_only=True)    

grouped = tips.groupby(["day", "smoker"], as_index=False)
grouped.mean(numeric_only=True)    











