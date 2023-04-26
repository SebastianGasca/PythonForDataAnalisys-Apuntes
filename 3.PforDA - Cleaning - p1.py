#--
#Handling Missing Data y Data Transformation. 
#--
import pandas as pd
import numpy as np

# ---- # ---- # ----
# 7.1 Handling Missing Data
#Definimos los valores nulos como 
na1 = None
pd.Series([1,2,na1])

na2 = np.nan
pd.Series([1,2,na2])

#Consultamos si hay valores nulos
float_data = pd.Series([1.2, -3.5, np.nan, 0])

df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5],
                   [np.nan, np.nan], [0.75, -1.3]],
                   index=["a", "b", "c", "d"],
                   columns=["one", "two"])

float_data.isna()                           #En una Serie
df.isna()                                   #En un DataFrame

#La forma negativa de consultar si hay NA es con .notna()
float_data.notna()

#Podemos rellenar valor Na con .fillna()
float_data.fillna(0)

# ---- # ---- # ----
# 7.1.1 Filtering Out Missing Data
#Podemos filtar los NA en una Serie por el metodo .dropna() o por consulta de vector booleano
data = pd.Series([1, np.nan, 3.5, np.nan, 7])

data.dropna()           #metodo .dropna()
data[data.notna()]      #consulta de vector booleano()

#Cuando eliminamos Na en un DataFrame podemos eliminar todas LAS FILAS que contengan "algun" NA o que 
#"todos" sus valores sean NA
data = pd.DataFrame([[1., 6.5, 3.], [1., np.nan, np.nan],
                     [np.nan, np.nan, np.nan], [np.nan, 6.5, 3.]])

data.dropna()               #Elimina todas las filas que contengan "algun" NA
data.dropna(how="all")      #Elimina todas las filas que contengan "todos" NA

#Podemos analizar los NA no por filas sino POR COLUMNAS
data[4] = np.nan; data
data.dropna(axis="columns", how="all")

#En caso de que queramos eliminar las filas que solo contengan un cierto numero de NA podemos
#configurarlo con el parametro "thresh"
df = pd.DataFrame(np.random.standard_normal((7, 3)))
df.iloc[:4, 1] = np.nan
df.iloc[:2, 2] = np.nan
df.dropna(thresh=2)

# ---- # ---- # ----
# 7.1.2 Filling In Missing Data
# En vez de descartar las filas o columnas que poseen NA, podemos rellenarlas con algun valor
df.fillna(0)                #Rellenamos con 0 los NA
df.fillna(df[1].mean())     #Rellenamos con la media de la columna "1"

#Usando un Diccionario como parametro podemos controlar con que valor rellenar cada columna
df.fillna({1: 0.5, 2: 0})

#Podemos interpolar los valores de relleno
df = pd.DataFrame(np.random.standard_normal((6, 3))); df
df.iloc[2:, 1] = np.nan; df
df.iloc[4:, 2] = np.nan; df

df.fillna(method="ffill")           #Rellenamos la columna con el ultimo valor que no fue NA
df.fillna(method="ffill", limit=2)  #Podemos poner un limite a la cantidad de valores a rellenar 




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 7.2 Data Transformation

# ---- # ---- # ----
# 7.2.1 Removing Duplicates
#Podemos consultar que valor esta duplicado.
data = pd.DataFrame({"k1": ["one", "two"] * 3 + ["two"],
                     "k2": [1, 1, 2, 3, 3, 4, 4]}); data

#El metodo .duplicated dira True en caso de que los valores de todas las columnas sean iguales.
#Ademas el segundo valor se considerara el duplicado.
data.duplicated()   

#Podemos eliminar los duplicados con .drop_duplicates()
data.drop_duplicates()

#Podemos considerar los duplicados solo para una columna. Ej #Quitamos las filas duplicadas cuando 
#existe un duplocado en "K1"
data["v1"] = range(7); data
data.drop_duplicates(subset=["k1"]) 

#El metodo siempre considera el elemento posterior a la primera combinacion como el duplicado. 
#Podemos cambiar esto manteniendo con el atributo "keep"
data.drop_duplicates(subset=["k1", "k2"], keep="last") 

# ---- # ---- # ----
# 7.2.2 Transforming Data Using a Function or Mapping
#En ocaciones queremos crear una variable en funcion al comportamiento de otras.
#Crearemos una columna que indique el animal del cual proviene un tipo de comida
data = pd.DataFrame({"food": ["bacon", "pulled pork", "bacon",
                              "pastrami", "corned beef", "bacon",
                              "pastrami", "honey ham", "nova lox"],
                              "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
data

#Por medio de un diccionario podemos otorgar las condiciones
meat_to_animal = {
  "bacon": "pig",
  "pulled pork": "pig",
  "pastrami": "cow",
  "corned beef": "cow",
  "honey ham": "pig",
  "nova lox": "salmon"
}

data["animal"] = data["food"].map(meat_to_animal); data

#Lo mismo que hicimos anteriormente pero de una forma mas clara
def get_animal(x): return meat_to_animal[x]
data["food"].map(get_animal)

# ---- # ---- # ----
# 7.2.3 Replacing Values
#Vimos que con el metodo .fillna() podemos rellenar los valores nulos.
#El metodo .replace() es una funcion mas general que la anterior.
data = pd.Series([1., -999., 2., -999., -1000., 3.])
data.replace(-999, np.nan)                          #Remplazamos los -999 por NA
data.replace([-999, -1000], np.nan)                 #Remplazamos los -999 y -1000 por NA

#Podemos asignar un valor de remplazo distinto para cada ocacion.  
data.replace({-999: np.nan, -1000: 0})              


# ---- # ---- # ----
# 7.2.4 Renaming Axis Indexes
#Al igual que los valores de una Serie, podemos transformar los valores de un indice por medio 
#de funciones (ayudarnos con metodos map). 
#Las transformaciones son "in place"

data = pd.DataFrame(np.arange(12).reshape((3, 4)),
                    index=["Ohio", "Colorado", "New York"],
                    columns=["one", "two", "three", "four"])

def transform(x): return x[:4].upper()
data.index = data.index.map(transform); data

#Podemos hacer lo mismo sin modificar el original con el metodo .rename(). 
#El metodo .rename() nos entrega una copia

#Aplicando funciones
data.rename(index=str.title, columns=str.upper)

#Aplicando relaciones por medio de diccionarios
data.rename(index={"OHIO": "INDIANA"}, columns={"three": "peekaboo"})


# ---- # ---- # ----
# 7.2.5 Discretization and Binning
#Las variables continuas se pueden discretizar usando conjuntos
#La funcion pd.cut() nos divide una variable continua en segmentos predefinidos. 
#Nos entrega un objeto de tipo categorico. 
#Los conjuntos son abiertos por la izquierda y cerrados por la derecha. 

ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
age_categories = pd.cut(ages, bins); age_categories

#Podemos explorar el objeto categorico
age_categories.codes        #Observar los niveles
age_categories.categories   #Observar las categorias

#Podemos contar la presencia de los grupos con la funcion pd.values_count() o su metodo
pd.value_counts(age_categories)   #Por funcion
age_categories.value_counts()     #Por metodo

#Podemos cambiar el hecho de que el connjunto sea cerrado por la derecha.  
pd.cut(ages, bins, right=False)

#Podemos asignarle un etiqueta a cada grupo
group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior"]
pd.cut(ages, bins, labels=group_names)

#Si a la funcion pd.cut() le asignamos un escalar, nos dividira la Serie en n segmentos uniformes
#(ordena de menor a mayor los numeros y corta la recta en n segmentos)
data = np.random.uniform(size=20)
uniform = pd.cut(data, 4, precision=2)    #La presicion indica el numero de decimal a considerar

uniform.categories
pd.value_counts(uniform)

#Tenemos la funcion pd.qcut() que nos divide la Serie en quantiles
#(ordena la recta de menor a mayor y corta la recta en n segmentos con la misma cantidad de datos)
data = np.random.standard_normal(1000)
quartiles = pd.qcut(data, 4, precision=2)

quartiles.categories
pd.value_counts(quartiles)

#A la funcion pd.qcut() podemos pasarle los quantiles que queremos utilizar como cortes
pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.]).value_counts()


# ---- # ---- # ----
# 7.2.6 Detecting and Filtering Outliers
data = pd.DataFrame(np.random.standard_normal((1000, 4)))
data.describe()

#Analizamos una Serie
col = data[2]         
col[col.abs() > 3]                          #Que valor son mayor a 3 en valor a absoluto?

#Analizamos un DF
data[data.abs() > 3]
data[(data.abs() > 3).any(axis="columns")]  #Que valor es mayor a 3 en valor absoluto en alguna las cols?

# ---- # ---- # ----
# 7.2.7 Permutation and Random Sampling
#Podemos reordenar aleatoriamente los elementos de una Serie o las filas de un DataFrame
#Usamos np.random.permutation() para seleccionar los indices de forma aleatorio

df = pd.DataFrame(np.arange(5 * 7).reshape((5, 7)))
sampler = np.random.permutation(5); sampler         

#Usamos .take() o .iloc[] para reordenar los valores de la Serie o las filas de un Dataframe
df.take(sampler)                                    
df.iloc[sampler]

#Podemos permutar las columnas tambien.
column_sampler = np.random.permutation(7)
df.take(column_sampler, axis="columns")
df.iloc[:,column_sampler]

#Podemos tomar muestras de una Serie o DataFrame
df.sample(n=3)

#Podemos tomar muestras con remplazo
choices = pd.Series([5, 7, -1, 6, 4])
choices.sample(n=10, replace=True)

# ---- # ---- # ----
# 7.2.8 Computing Indicator/Dummy Variables
#Podemos transformar las variables categoricas como Dummys
df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"],
                   "data1": range(6)})
df

#Transformamos una Serie en una matriz de 0s y 1s indicando la presencia o ausencia 
#de un elemento de la Serie
pd.get_dummies(df["key"])

#Podemos agregarle un prefijo a los nombres de las columnas
dummies = pd.get_dummies(df["key"], prefix="key"); dummies

#La volvemos a pegar con las demas columnas de su DF original
df_with_dummy = df[["data1"]].join(dummies); df_with_dummy

#Podemos usar pd.get_dummies() con pd.cut()
np.random.seed(12345)
values = np.random.uniform(size=10); values

bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
pd.get_dummies(pd.cut(values, bins))


