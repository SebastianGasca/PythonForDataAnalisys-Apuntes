#--
#Reshaping and Pivoting
#--
import pandas as pd
import numpy as np

# ---- # ---- # ----
# 8.3 Reshaping and Pivoting
#Hay formas de reordenar los "datos tabulares" (los DataFrames). Estas son conocidos como operaciones "reshape" o "pivoting" 

# ---- # ---- # ----
# 8.3.1 Reshaping with Hierarchical Indexing
# Los indices jerarquicos nos proveen formas consistentes de reordenar los datos en un DF.

# Stack: Pivotea de columnas a filas (pivot_longer en R)
# Unstack: Pivotea de filas a columnas (pivot_winder e R)

data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                    index=pd.Index(["Ohio", "Colorado"], name="state"),
                    columns=pd.Index(["one", "two", "three"], name="number"))
data

# Stack nos permite dejar las columnas en una variable que las contenga, formando la combinacion 
# entre las filas y columnas necesarias. Pasamos de ub DF a una Serie con indices jerarquicos.
result = data.stack(); result 
isinstance(result, pd.Series)

# Unstack es la contraposicion de Stack. Pasamos de la Serie a DF nuevamente. 
result.unstack()

# Por defecto el nivel mas interno es el unstacked. Podemos cambiar esto con el parametro "level="
result.unstack(level=0)
result.unstack(level="state")

# Realizar .unstack a un DF puede producir valores nulos si no se encuentran los valores para algun nivel
s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"], dtype="Int64")
s2 = pd.Series([4, 5, 6], index=["c", "d", "e"], dtype="Int64")
data = pd.concat([s1, s2], keys=["one", "two"]); data
data.unstack()

# Si volvemos de .unstack() con .stack() omitimos por defecto los NA. Podemos evitar esto por "dropna="
data.unstack().stack()
data.unstack().stack(dropna=False)


# ---- # ---- # ----
# 8.3.2 Pivoting “Long” to “Wide” Format
#Es comun almacener datos en el llamado "long or stacked format". Valores individuales son representados
#por una sola fila en vez de multiples valores por filas. Ej
data = pd.read_csv("./macrodata.csv")
data = data.loc[:, ["year","quarter","realgdp","infl","unemp"]]; data

#Vamos a unir las columnas de "year" y "quarter". El metodo .pop descarta 
#las columnas del Dataframe "data" al mismo tiempo que rescatamos los datos
periods = pd.PeriodIndex(year=data.pop("year"),
                         quarter=data.pop("quarter"),
                         name="date")

data.index = periods.to_timestamp("D"); data.index
data.head()

#Agregamos un nombre a los indices de las columnas
data.columns.name = "item"; data

#Ahora vamos a "apilar" los datos para formar un DFs con "long format".
#Recordar que usamos .reset_index() debido a que nuestro resultado al aplicar el metodo .stack() es una Serie. 
long_data = (data.stack()
             .reset_index()
             .rename(columns={0: "value"}))
long_data

# Ahora a lo que nos convoca:
# Es posible que trabajar con datos en "long format" no nos sea util, en estos casos tenemos un metodo en pandas 
# llamada .pivot() para pasar de "long" to "wide" format.
# Ojo que nos pide ingresar una columna que quedara como indice, en todo caso podemos usar .reset_index()
# Ojo que la columna con la cual se generaran las otras columnas quedara de nombre para los indices de columnas
pivoted = long_data.pivot(index="date", columns="item", values="value"); pivoted

# Es posible que queramos pivotear mas de una columna de valores, como como se comporta a lo largo del tiempo
# las variables en dos casos distintos. En este caso podemos: 
long_data["value2"] = np.random.standard_normal(len(long_data))
pivoted = long_data.pivot(index="date", columns="item", values=["value","value2"])

# ---- # ---- # ----
# 8.3.3 Pivoting “Wide” to “Long” Format
# A la inversa del metodo .pivot() tenemos .melt(). En vez de transformar
# una columna en varias, une multiples columnas en una sola. 

df = pd.DataFrame({"key": ["foo", "bar", "baz"],
                   "A": [1, 2, 3],
                   "B": [4, 5, 6],
                   "C": [7, 8, 9]})
df

#Hay que identificar que variable sera el indicar de grupo. En el ejemplo usaremos
#la columna "key". 
melted = df.melt(id_vars="key")

#Podemos pasar de un "long format" a "wide format" usando .melt() y luego .pivot().
#En el siguiente ejemplo volvemos al DataFrame original ("df")
reshaped = melted.pivot(index="key", columns="variable", values="value"); reshaped

#Podemos hacer pasar el indice a columna
reshaped.reset_index()

#Si querermos podemos "apilar" solo algunas columnas. (en el siguiente ejemplo usamos
#la funcion pd.melt())
pd.melt(df, id_vars="key", value_vars=["A", "B"])

#Si queremos no usamos identificador de grupo ("id_vars")
pd.melt(df, value_vars=["key", "A", "B"])



