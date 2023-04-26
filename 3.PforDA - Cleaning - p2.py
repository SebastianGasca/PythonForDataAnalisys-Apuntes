#--
#Extension Data Types, String Manipulation y Categorical Data. 
#--
import pandas as pd
import numpy as np
# ---- # ---- # ----
# 7.3 Extension Data Types
#Pandas fue construido sobre las capacidades presentes en Numpy, una libreria 
#de computacion vectorial usada principalmente para trabajar con data numerica.

#La construccion sobre Numpy trae algunas deficiencias
#1. El manejo de Missing Data para algunos tipos de datos numericos (entero y 
#   flotantes) fue incompleto
#2. Archivos con muchos datos tipo string eran computacionalmente pesados usando
#   mucha memoria
#3. Algunos tipos de datos como time intervals, timedeltas y timestamps con zonas
#   horarios no podian ser soportados eficientemente sin usar vectores muy costosos
#   en rendimiento hechos de Python Objects
#Mas recientemente Pandas desarrollo un sistema de extension types. 

#A pesar de que es una vector de enteros con un NA el tipo es Float64
s = pd.Series([1, 2, 3, None])
s.dtype

#Podemos cambiar el tipo de datos, usando la funcion de pandas pd.Int64Dtype() 
#como su forma abreviada "Int64" son validas 
s = pd.Series([1, 2, 3, None], dtype=pd.Int64Dtype())
s = pd.Series([1, 2, 3, None], dtype= "Int64")
s.dtype

#Pandas tambien tiene un "extencion type" especializado para string. 
#Usar esta extencion consume menos memoria y computacionalmente son mas eficientes
s = pd.Series(['one', 'two', None, 'three'], dtype=pd.StringDtype())
s.dtype

#Podemos modificar los tipos de datos de una Serie por el metodo .astype(). Util
#para cambiar tipos de un DF
df = pd.DataFrame({"A": [1, 2, None, 4],
                   "B": ["one", "two", "three", None],
                   "C": [False, None, False, True]})

df["A"] = df["A"].astype("Int64")
df["B"] = df["B"].astype("string")
df["C"] = df["C"].astype("boolean")
df.dtypes




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 7.4 String Manipulation

# ---- # ---- # ----
# 7.4.1 Python Built-In-String Object Method
#Muchas veces las funciones nativas de string de Python son suficientes para trabajar con string
val = "a,b,  guido"

val.split(",")                                  #.split() separa un string por caracter
pieces = [x.strip() for x in val.split(",")]    #.strip() elimina los white spaces

first, second, third = pieces   
first + "::" + second + "::" + third            #Podemos concadenar string con "+"

#Una forma mas eficientes es usando .join() para unir una lista o tupla de string
"::".join(pieces)

#Tenemos algunos metodos conocidos como de locacion
"guido" in val                                  #Existe el substring "guido" en val?

val.index(",")                                  #El indice de posicion del caracter
val.find(":")                                   #Lo mismo que index, pero en caso de no estar da -1

val.count(",")                                  #Numero de ocurrencias de una substring


#Podemos substituir un caracter por otro con .replace()
val.replace(",", "")


# ---- # ---- # ----
# 7.4.2 Regular Expression
#Las Regex nos proveen una forma flexible de encontrar patrones en los textos

#Los modulos de las Regex caen en 3 categorias: 
#1. Pattern Matching
#2. Substitution
#3. Splittng

import re

text = "foo    bar\t baz  \tqux"
re.split(r"\s+", text)              #Nos crea una lista de los elementos separados por la regex
re.findall(r"\s+", text)            #Nos crea una lista de los elementos que cumplen la regex

#Si usamos una misma regex para muchos analisis podemos compilarla. Esto lo hace mas eficiente
regex = re.compile(r"\s+")
regex.split(text)

#Tenemos algunos metodos comunes
#.search()  Usado para retornar el primer match
#.match()   Usado para retornar el primer match solo si esta al comienzo del texto
#.sub()     Usado para remplazar los elementos que hagan match con la regex por otro string
#


# ---- # ---- # ----
# 7.4.3 String Functions in Pandas
#Si aplicaramos un metodo .map() en conjunto con una funcion lambda podemos aplicar
#las funciones internas de python o regex para manipular string de un vector. Pero
#si existen NA fallaran. 
#Pandas posee una serie de metodos para trabajar con vectores compuestos de string

data = {"Dave": "dave@google.com", "Steve": "steve@gmail.com",
        "Rob": "rob@gmail.com", "Wes": np.nan}
data = pd.Series(data)
data.isna()

#Preguntamos si cada elemento contiene el string
data.str.contains("gmail") 
#Observemos que la respuesta es un objeto de tipo "object"                 

#Modificamos el vector que esta en tipo "object" a "string"
data_as_string_ext = data.astype("string")
data_as_string_ext.str.contains("gmail")
#Observamos que la respuesta es de tipo "boolean"

#Podemos usar metodos regex como .str.findall()
import re

pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"
data.str.findall(pattern, flags=re.IGNORECASE)

#Podemos acceder a los elementos por indices o .get()
matches = data.str.findall(pattern, flags=re.IGNORECASE).str[0]; matches

matches.str.get(1)
matches.str[1]

#Podemos acceder a los elementos de cada string del vector
data.str[:5]

#Podemos usar el metodo str.extract() que nos genera en vez de 
#una lista de tuplas como lo hace str.findall() un Data Frame
data.str.extract(pattern, flags=re.IGNORECASE)

#Hay muchos otros metodos que investigar. Se Podria ver la Tabla 7.5




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 7.5 Categorical Data

# ---- # ---- # ----
# 7.5.1 Background and Motivation
#En ocaciones tenemos vectores compuestos de pequeños grupos de valores
values = pd.Series(['apple', 'orange', 'apple','apple'] * 2); values
values.unique()
values.value_counts()

#Muchos sistemas de datos han desarrollado enfoques especializados para 
#representar datos con valores repetidos para una mejor eficiencia de 
#almacenamiento y computacion. 

#En los Data Warehousing una buena practica es usar las llamadas 
#"so-called dimension tables" 
values = pd.Series([0, 1, 0, 0] * 2); values
dim = pd.Series(['apple', 'orange']); dim

#Podemos usar .take() para restaurar la Serie original de String
dim.take(values)

#Esta representacion como enteros es la llamada representacion "categorical" o "dictionary-encoded". 
#El vector de valores distintos es llamado "categories", "dictionary" o "leves of data".

# ---- # ---- # ----
# 7.5.2 Categorical Extension Type in pandas
#Pandas tiene un tipo de extencion especial para mantener los datos que usan "the integer-based 
#categorical representation" o "encoding"

fruits = ['apple', 'orange', 'apple', 'apple'] * 2; fruits
N = len(fruits); N

rng = np.random.default_rng(seed=12345)
df = pd.DataFrame({'fruit': fruits,
                   'basket_id': np.arange(N),
                   'count': rng.integers(3, 15, size=N),
                   'weight': rng.uniform(0, 4, size=N)},
                   columns=['basket_id', 'fruit', 'count', 'weight'])
df

#Podemos convertir la Serie df["fruit"] de tipo string en una tipo categorica
fruit_cat = df['fruit'].astype('category')
fruit_cat                                       #Ahora es de tipo categorico

#Accedemos al vector de datos categoricos de la serie con .array
c = fruit_cat.array

c.categories
c.codes

#Un truco para visualizar los niveles de cada categoria es
dict(enumerate(c.categories))

#Podemos convertir la columna de un DF en categorico
df['fruit'] = df['fruit'].astype('category')
df["fruit"]

#Podemos crear un pd.Categorical desde una secuencia de datos. 
#Si observamos por medio de .categories tenemos que las categorias estan ordenadas por alfabeto 
my_categorias = pd.Categorical(["foo","bar","baz","foo","bar"]); my_categorias

my_categorias.categories                        
my_categorias.codes

#Podemos crear un pd.Categorical desde una secuencia de numeros con asignacion de etiquetas.
#Ahora el orden no sera por orden alfabetico, sino que por como dispongamos el vector de etiquetas
codes = [0, 1, 2, 0, 0, 1]
categories = ['foo', 'bar', 'baz']
my_cats_2 = pd.Categorical.from_codes(codes, categories); my_cats_2

my_cats_2.categories
my_cats_2.codes

#Podemos asignar un orden jerarquico sobre las cateogorias
ordered_cat = pd.Categorical.from_codes(codes, categories, ordered=True)
ordered_cat


# ---- # ---- # ----
# 7.5.3 Computing with Categorical
#Algunas partes de pandas, como la funcion "groupby", tienen una performance mejor cuando trabajamos
#con datos categoricos.

#Trabajemos con la funcion qcut() vista anteriormente 
rng = np.random.default_rng(seed=12345)
draws = rng.standard_normal(1000)

bins = pd.qcut(draws, 4); bins.dtype          
bins.value_counts()

#Nos acomoda colocarle nombres a los contenedores numericos
bins = pd.qcut(draws, 4, labels=["Q1", "Q2", "Q3","Q4"]); bins.dtype     

bins
bins[0:10]
bins.codes[0:10]

#A pesar de que los esten asociados a un nivel, no tienen asociados valores mas complejos por grupos. 
#Usamos "groupby" para obtener informacion de las categorias
bins = pd.Series(bins, name='quartile'); bins
results = (pd.Series(draws)
           .groupby(bins)
           .agg(['count', 'min', 'max'])
           .reset_index())
results

#Como dijimos los datos de tipo Categoricos poseen mejor performance y uso de memoria. vemos el sgte ej:
N = 10_000_000

labels = pd.Series(['foo', 'bar', 'baz', 'qux'] * (N // 4))
categories = labels.astype('category')

#"labels" usa mas memoria que "categories"
labels.memory_usage(deep=True)                  
categories.memory_usage(deep=True)                                           

#Usar groupby es mucho mas rapido con datos categoricos. (Usamos values.counts() que trabajo bajo groupby)
#%timeit labels.value_counts()
#%timeit categories.value_counts()

# ---- # ---- # ----
# 7.5.4 Categorical Method
#Las Series que contiene datos categoricos posee especiales metodos similar a los metodos 
#especiales de Series.str
s = pd.Series(['a', 'b', 'c', 'd'] * 2)
cat_s = s.astype('category'); cat_s

#El metodo especial ".cat" nos da acceso a los metodos para trabajar con categorias
#(al igual que .str para metodos de string)

#Revisamos los niveles
cat_s.cat.codes

#Podemos asignar un nuevo vector de categorias a una Serie de datos categoricos
actual_categories = ['a', 'b', 'c', 'd', 'e']
cat_s2 = cat_s.cat.set_categories(actual_categories); cat_s2

#Aunque pareciera que lo anterior no modifico nada, la nueva categoria aparecera en operaciones donde la usen
cat_s.value_counts()
cat_s2.value_counts()

#En grandes datasets, las categorias son usadas para guardar memoria y poseer mejor performance. Pero
#luego de hacer algunos filtros, muchas de las categorias ya no aparece en la data. 
#Podemos usar el metodo ".remove_unsed_categories" para eliminar las categorias no observadas.
cat_s3 = cat_s[cat_s.isin(['a', 'b'])]; cat_s3
cat_s3.cat.remove_unused_categories()










