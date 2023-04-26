import numpy as np
import pandas as pd

# ---- # ---- # ----
# 1.1 Series
#Las series son como los array pero con una columna de etiqueta (indice)
obj = pd.Series(np.arange(10)) ; obj

#Accedemos a sus valores y su indice. El resultado es un array de numpy con algunas caracteristicas especiales 
obj.array
obj.index

#Por dejecto el indice de una Serie es numerico, podemos modificar eso
obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"]) ; obj2

#Podemos accedemos a los valores de una serie por medio de indices o su etiqueta
obj2[1]
obj2["b"]

obj2[["b", "c"]]

#Podemos usar funciones de numpy sobre una Serie
np.exp(obj2)

#Podemos aplicar metodos de vectorizacion a una Serie
obj2 * 2

#Podemos filtar por vectores booleanos 
obj2[obj2 > 0]

#Podemos preguntar si una etiqueta (indice) se encuentra en nuestra serie
"b" in obj2

#Podemos crear Series a partir de Diccionarios
sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
obj3 = pd.Series(sdata); obj3

#Tambien podemos crear Diccionarios a partir de Series
obj3.to_dict()                               

#Cuando creamos series a partir de Diccionarios, las etiquetas quedan 
#en el orden en el que vienen del Diccionario. Podemos modificar esto
states = ["California", "Ohio", "Oregon", "Texas"]
obj4 = pd.Series(sdata, index=states); obj4      
#como California no se encuentra en el diccionario queda como NA y Utah desaparece

#Podemos verificar valores NA con las funciones de pandas pd.isna(), or por los metodos .isna()
pd.isna(obj4)
pd.notna(obj4)

obj4.isna()

#Si sumamos dos series se relacionara cada elemento entre ella por medio de sus indice
obj3
obj4

obj3 + obj4

#Podemos colocarle nombres tanto a la Serie como a su "columna" de indice
obj4.name = "poblacion"; obj4
obj4.index.name = "state"; obj4

#El cambio de etiqueta en el indice es "in place"
obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"]) 
obj2.index = ["Bob", "Steve", "Jeff", "Ryan"]; obj2






# ---- # ---- # ----
# 1.2 Data Frame (DF)

#Podemos construir un DF desde un Diccionario
data = {"state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002, 2003],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}

frame = pd.DataFrame(data); frame

#Podemos seleccionar las primeras o ultimas filas
frame.head()
frame.tail()

#Al igual que en la serie, podemos ordenar las columnas de un DF al momento de ser creado
pd.DataFrame(data, columns=["year", "state", "pop"])

#Al igual que en la serie, si pasamos columnas que no pertencen seran nulas
frame2 = pd.DataFrame(data, columns=["year", "state", "pop", "debt"]); frame2

#Accedemos a una columna de un DF por medio del nombre. La columna retornada es solo una visualizacion, no una copia
frame2["year"]
frame2.year

#Accedemos a una fila de un DF por medio de su nombre (.loc) o un indice (.iloc)
frame2.loc[1] 
frame2.iloc[1]

#Podemos rellenar las columnas por asignacion escalar o array
frame2["debt"] = 16.5 ; frame2              
frame2["debt"] = np.arange(6); frame2       #(debe coincidir en el largo)

#Si queremos rellenar una columna por medio de una Serie, los indice de la Serie y el DF deben coincidir
val = pd.Series([-1.2, -1.5, -1.7], index=["two", "four", "five"]); val
frame2["debt"] = val ; frame2

#Podemos rellenar las columnas por vectores booleanos
frame2["eastern"] = frame2["state"] == "Ohio"; frame2

#Podemos borrar columnas por medio del metodo DEL. La eliminacion es "in place"
del frame2["eastern"]; frame2
frame2.columns

#Podemos construir un DF por medio de Diccionarios de Diccionarios, la key mas interna representa el indice
populations = {"Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
               "Nevada": {2001: 2.4, 2002: 2.9}}
frame3 = pd.DataFrame(populations); frame3

#Otro metodo util es crear un DF por medio de una array 2x2
pd.DataFrame(np.arange(4).reshape(2,2)) 
#En la tabla 5.1 se pueden ver todas las formas de crear un DF.

#A diferencia de una Serie el DF no tiene un nombre asociado, pero si se pueden asignar nombres a su indice y columnas
frame3.index.name = "year"
frame3.columns.name = "state"
frame3

#Trasponemos un DF al igual que un array de Numpy
frame3.T

#Al igual que las Series podemos pasar de un DF a diccinario o array de numpy
frame3.to_dict()
frame3.to_numpy() 





# ---- # ---- # ----
# 1.3 Index Objects
#El Index Objects son los encargado de mantener las etiquetas de los datos tanto en los indices y columnas
#como en su metadata (los nombres asociados a ellas)

#Los indices son inmutables (a menos que se cambie todo el vector de indice)
obj = pd.Series(np.arange(3), index=["a", "b", "c"])
index = obj.index

index[1]
index[1] = "d"      #No podemos cambiar un valor del indice


#Podemos craar un objeto tipo indice y asignarlo como indice en la construccion de una Serie o DF
labels = pd.Index(np.arange(3)); labels
obj2 = pd.Series([1.5, -2.5, 0], index=labels)

#Podemos consultar si un elemento esta en algun indice
frame3

"Ohio" in frame3.columns
2002 in frame3.index

#Los indices pueden contener valores duplicados (esto es debido a que podemos tener indice multinivel)
pd.Index(["foo", "foo", "bar", "bar"])

#Existen diferentes funciones para trabajar con indices
frame3
ic = frame3.columns; 

ic.append(pd.Index(["Santiago"]))       #sumamos un indice

ic.intersection(pd.Index(["Ohio"]))     #seleccionamos solo los indices que coinciden
ic.difference(pd.Index(["Ohio"]))       #seleccionamos solo los indices que no coinciden

ic.isin(pd.Index(["Ohio"]))             #generamos un vector booleano indicando si cada valor contenido existe o no

#Se pueden ver mas metodos en la tabla 5.2




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# 2 Essential Functionality

# ---- # ---- # ----
# 2.1 Reindexing
#Podemos reordenar los indices de una Serie ya creada con el metodo .reindex()

obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=["d", "b", "a", "c"]); obj
obj2 = obj.reindex(["a", "b", "c", "d", "e"]); obj2

#Si queremos agregar un indice mas largo que la cantidad de filas de una Serie
#podemos interpolar los valores para que se logre el largo del indice

obj3 = pd.Series(["blue", "purple", "yellow"], index=[0, 2, 4]); obj3
obj3.reindex(np.arange(6), method="ffill")

#Como se menciono antes podemos reordenar los indices o columnas de DF con los atributos index o columns
frame = pd.DataFrame(np.arange(9).reshape((3, 3)), 
                     index=["a", "c", "d"], 
                     columns=["Ohio", "Texas", "California"]); frame


frame.reindex(index=["a", "b", "c", "d"])                   #indice
frame.reindex(columns=["Texas", "Utah", "California"])      #columna

#Algunos atributos del metodo reindex()
frame.reindex(["Texas", "Utah", "California"], axis="columns")  # por medio del atributo axis podemos definir 
                                                                # si nos referimos a columnas o filas       
                                                                                                                 
frame.reindex(index=["a", "b", "c", "d"], fill_value=1)         # fill_value : rellena los NA con un valor
frame.reindex(index=["a", "b", "c", "d"], copy=True)            # copy : asegura que se copie la Serie o DF





# ---- # ---- # ----
# 2.2 Dropping Entries from an Axis

#Podemos eliminar filas de una Serie por el metodo .drop()
obj = pd.Series(np.arange(5.), index=["a", "b", "c", "d", "e"]); obj

obj.drop("c") 
obj.drop(["d", "c"])

#Podemos hacer esto mismo en un DF
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=["Ohio", "Colorado", "Utah", "New York"],
                    columns=["one", "two", "three", "four"])
data

data.drop(index=["Colorado", "Ohio"])
data.drop(columns=["one", "three"])
data.drop(["two", "four"], axis="columns")





# ---- # ---- # ----
# 2.3 Indexing, Selection, and Filtering

#Acceder a los elementos de una Serie funciona igual que un array de numpy
obj = pd.Series(np.arange(4.), index=["a", "b", "c", "d"])

obj["b"]                #por etiqueta
obj[1]                  #por indice
obj[["b", "a", "d"]]    #por grupo de etiqueta
obj[2:4]                #por rango
obj[obj < 2]            #por vector booleano


#La forma mas comun de acceder a los datos es usando los metodos .loc[] y .iloc[]
#ya que aseguramos que por medio de .loc[] vamos a utilizar etiquetas y por .iloc[] indices

obj1 = pd.Series([1, 2, 3], index=[2, 0, 1]); obj1
obj2 = pd.Series([1, 2, 3], index=["a", "b", "c"]); obj2

obj1.loc[[2,0,1]]               #accedemos por medio de sus etiquetas
obj2.loc[["a", "b", "c"]]       

obj1.iloc[[0,1,2]]              #accedemos por medio de sus indices
obj2.iloc[[0,1,2]]       

#Podemos utilizar .loc[] para selecciones por rango
obj2.loc["b":"c"]


#Haciendo selecciones para un DF tenemos
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=["Ohio", "Colorado", "Utah", "New York"],
                    columns=["one", "two", "three", "four"])

data["two"]                     #Por etiqueta tenemos las columnas             
data[["two", "one"]]            

data[:1]                        #Por numero tenemos las filas (hay que usar ":")
data[:2]            

data["three"] > 5
data[data["three"] > 5]         #Por medio de vector booleano

data[data < 5] = 0; data        #Asignamos "in place"

# ---- # ---- # ----
# 2.3.1 Selection on DataFrame with loc and iloc
#Como se menciono tenemos los metodos .loc[] y .iloc[] para acceder a las filas y columnas de un DF
data

#Usando el metodo .loc[] usamos etiquetas
data.loc["Colorado"]                    #Accedemos a filas              
data.loc[["Colorado", "New York"]]      

data.loc[:,["one", "two"]]              #Accedemos columnas

data.loc[["Colorado"], ["one"]]         #Aceddemos a filas y columnas

#Usando el metodo .iloc[] usamos indices
data.iloc[2]
data.iloc[[2, 1]]

data.iloc[2, [3, 0, 1]]
data.iloc[[1, 2], [3, 0, 1]]

#Podemos hacer filtros compuestos. Primero seleccionamos por .iloc[], luego por un filtro con vector booleano
data.iloc[:, :3][data.three > 5]

#Para filtar por vector booleano usando los metodos loc[] y iloc[], solo podemos hacerlo con loc[]
data.iloc[data.three >= 2] #Dara error
data.loc[data.three >= 2]

# ---- # ---- # ----
# 2.3.2 Integer indexing pitfalls
# Hay algunas trampas que considerar al momento de hacer indexing
ser = pd.Series(np.arange(3.))
ser[-1] #nos data error

ser2 = pd.Series(np.arange(3.), index=["a", "b", "c"])
ser2[-1] #no nos data error

#Por eso es util usar los metodos .loc[] o .iloc[]. #Si usamos el metodo .iloc[] no nos data error 
ser.iloc[-1] 

# ---- # ---- # ----
# 2.3.3 Pitfalls with chained indexing
data
data.loc[:, "one"] = 1                  #a la columna "one" asignamos 1

data["four"] > 5
data.loc[data["four"] > 5] = 3; data    #en las filas donde los valores de la columna "four" sean mayor a 5 se colocara 3

data.loc[data.three == 5, "three"] = 6  #en la fila donde el valor de la columna "four" sea igual a 5 y
                                        #ademas pertencezca a la columna "three" se colocara 6





# ---- # ---- # ----
# 2.4.1 Arithmetic and Data Alignment
# Al hacer aritmetica con Series o DF, la no relacion entre indices generara espacios nulos. De todas formas Pandas
# unira las Series o DataFrame

#En series
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=["a", "c", "d", "e"])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=["a", "c", "e", "f", "g"])

#Sumara donde coincidan los indices. En este caso seran "a", "c", "e". Los demas seran incluidos pero en NA
s1 + s2

#En DataFrame
df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list("bcd"),  
                   index=["Ohio", "Texas", "Colorado"]); df1
df2 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list("bde"), 
                   index=["Utah", "Ohio", "Texas", "Oregon"]); df2

#Sumara donde coincidan el par Indice, Columna. En caso contrario quedara en NA
df1 + df2

#Otro ejemplo. Da NA debido a que no coinciden en Columnas
df1 = pd.DataFrame({"A": [1, 2]})
df2 = pd.DataFrame({"B": [3, 4]})
df1 + df2      

# ---- # ---- # ----
# 2.4.2 Arithmetic methods with fill values

#Podemos rellenar los espacios en NA cuando hacemos aritmetica entre Series o DF y las combinaciones de indices no coinciden.
df1 = pd.DataFrame(np.arange(12.).reshape((3, 4)),
                   columns=list("abcd")); df1

df2 = pd.DataFrame(np.arange(20.).reshape((4, 5)),
                   columns=list("abcde")); df2

#Usamos el metodo .add() para sumar y el parametro fill_values para asignar valor
df1 + df2                       #sin relleno
df1.add(df2, fill_value=0)      #si df2 no posee valores en algun indice o columna de df1 entonces se rellena con cero

#Otro ejemplo. Usamos el metodo .reindex()
df1.reindex(columns=df2.columns, fill_value=0)

# ---- # ---- # ----
# 2.4.3 Operations between DataFrame and Series
frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),
                     columns=list("bde"),
                     index=["Utah", "Ohio", "Texas", "Oregon"])

series = frame.iloc[0]          #Primera fila del DF

#Cuando hacemos aritmetica entre Series y Dataframe por defecto se hace match entre los indices
#de la Serie y las columnas del Dataframe. Podemos pensarlo como un vector operando para cada fila 
# del DF
frame - series                  

#Si no se encuentra alguna columna en el DF o un indice en la Serie que coincidan se entregara un NA
series2 = pd.Series(np.arange(3), index=["b", "e", "f"])
frame - series2

#Si NO queremos que los indices de la Serie se relacionen con las columnas del DF y queremos que
#los indices de la Serie se relacionen con los indices del DF debemos usar algun metodo que simule
#una funcion aritmetica para colocar el parametro "axis"
series3 = frame["d"]; series3
frame.sub(series3, axis="index")





# ---- # ---- # ----
# 2.5 Function Application and Mapping

# Las funciones de numpy funcionan con pandas
frame = pd.DataFrame(np.random.standard_normal((4, 3)),
                     columns=list("bde"),
                     index=["Utah", "Ohio", "Texas", "Oregon"])
frame
np.abs(frame)

#Otras operaciones frecuentes es aplicar funciones en one-dimensional arrays para alguna Columna o Fila 
#En este ejemplo operamos la diferencia entre la media y el maximo para cada Columna del DF
#(cada Columna es una Serie y a cada una de ella se le aplica la funcion)
def f1(x): return x.mean() - x.min()
frame.apply(f1)

#Si quisieramos aplicar la misma funcion pero para cada fila del DF debemos cambiar el parametro "axis"
frame.apply(f1, axis="columns")

#La funcion que apliquemos en apply() puede no solo entregar valores escalares. En el siguiente ej
#la funcione entrega una Serie con el valor min y max, para cada columna que recorre. 
def f2(x): return pd.Series([x.min(), x.max()], index=["min", "max"])
frame.apply(f2)


#Aparte de utilizar funciones sobre vectores de una dimension (one-dimensional arrays) podemos
#aplicar Element-wise Python functions. 

#EJ. Vamos a dejar a cada uno de los valores del DF con solo dos decimales 
def my_format(x): return f"{x:.2f}"
frame.applymap(my_format)

#El metodo .applymap() se relaciona a los DataFrame. En caso de que queramos hacer algo parecido 
#para una Serie tenemos el metodo .map()
frame["e"].map(my_format)



# ---- # ---- # ----
# 2.6 Sorting and Ranking

#Podemos ordenar una Serie por su indice
obj = pd.Series(np.arange(4), index=["d", "a", "b", "c"])
obj.sort_index()

#Lo mismo para un DF. Aca podemos considerar un orden por indice o nombre de columnas
frame = pd.DataFrame(np.arange(8).reshape((2, 4)),
                     index=["three", "one"],
                     columns=["d", "a", "b", "c"])

frame.sort_index()                                      #por defecto ordena por indice
frame.sort_index(axis="columns")                        #ordenamos por nombre de columnas
frame.sort_index(axis="columns", ascending=False)       #ordenamos por nombre de columnas de forma descendente


#Podemos ordenar las Series en base a sus valores
obj = pd.Series([4, 7, -3, 2])
obj.sort_values()                                       #de menor a mayor

obj = pd.Series([4, np.nan, 7, np.nan, -3, 2])
obj.sort_values()                                       #los NA quedan al final
obj.sort_values(na_position="first")                    #los NA quedan al principio

#Podemos ordenar los DF en base a sus valores
frame = pd.DataFrame({"b": [4, 7, -3, 2], 
                      "a": [0, 1, 0, 1]})

frame.sort_values("b")                                  #Ordenamos en base a los valores de la col "b"
frame.sort_values(["a", "b"])                           #Ordenamos en base a los valores de la col "a" y "b"


#Podemos rankear una serie o columna de DF.   
#Rankear una Serie indica que de manera interna se ordenan los valores de menor a mayor, luego 
#a cada uno de los valores se le asigna un nivel y ese nivel sera el entregado en respuesta al 
#valor de la Serie. 

#El rankeo dependera  del metodo asociado, ya que si dos valores poseen el mismo valor estaran 
#dentro del mismo nivel en ranking, por ende se entregara por ejemplo la media o el primer valor
#dependiendo del metodo (hay mas metodos)    

obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
obj.rank()                                      #por defecto el metodo utilizado es de la media
obj.rank(method="first")                        #asignamos metodo del primer valor
obj.rank(ascending=False)                       #el orden es descendente

#Si trabajamos sobre un DF podemos hacer rankeo sobre cada una de las filas
frame = pd.DataFrame({"b": [4.3, 7, -3, 2], "a": [0, 1, 0, 1],
                      "c": [-2, 5, 8, -2.5]})

frame.rank(axis="columns")





# ---- # ---- # ----
# 2.7 Axis Indexes with Duplicate Labels
#Para saber si nuestra Serie o DF no posee indices/etiquetas unicas podemos hacer la consulta
obj = pd.Series(np.arange(5), index=["a", "a", "b", "b", "c"])
obj.index.is_unique

obj["a"]
obj["c"]




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 3 Summarizing and Computing Descriptive Statistics
#Los objetos de pandas vienen con metodos matematicos y estadisticos incluidos. 
df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5],
                   [np.nan, np.nan], [0.75, -1.3]],
                   index=["a", "b", "c", "d"],
                   columns=["one", "two"])

df
df.sum()                        #se suman los valores por filas (de arriba hacia abajo)
df.sum(axis="columns")          #se suman los valores por columnas (de izquierda a derecha)

df.sum(axis="index", 
       skipna=False)            #podemos incluir no saltarnos los NA. La suma dara NA en caso de existir
      
df.mean(axis="columns")                                

#Tenemos algunos metodos de acumulacion
df.cumsum()

#Metodos de resumen estadisticos
df.describe()                                   #datos numericos
df.quantile(q=[.5,.8])

obj = pd.Series(["a", "a", "b", "c"] * 4)
obj.describe()                                  #datos no numericoas

#Metodo de las diferencias porcentuales
df
df.pct_change()                                 #b de la columna one, vario un 407%


# ---- # ---- # ----
# 3.1 Correlation and Covarianza
#Con variables numericas podemos obtener la correlacion entre ellas

price = pd.read_pickle("examples/yahoo_price.pkl")
volume = pd.read_pickle("examples/yahoo_volume.pkl")
returns = price.pct_change()

returns["MSFT"].corr(returns["IBM"])            #correlacion entre las columnas MSFT y IBM
returns["MSFT"].cov(returns["IBM"])             #covariacion entre las columnas MSFT y IBM                     

returns.corr()                                  #matriz de correlacion 
returns.cov()                                   #matriz de covariacion

#Podemos correlacionar con otras Series o DataFrame
returns.corrwith(returns["IBM"])
returns.corrwith(volume)


# ---- # ---- # ----
# 3.3 Unique value, Value Counts, and Mermbership
#Valores unicos
obj = pd.Series(["c", "a", "d", "a", "a", "b", "b", "c", "c"])
uniques = obj.unique() ; uniques

#Contar valores. Util para resumir categoricos (igual sirve para numericos, seria algo como un hist).
#Si lo aplicamos a una Serie el indice indica la variable categorica o numerica a contar 
obj.value_counts()

#Existe tambien la funcion pd.values_counts() para ingresar como input array de numpy o listas de python
pd.value_counts(obj.to_numpy(), sort=False)

#Podemos verificar si elementos pertenecen o no a una Serie o Columna de DataFrame con el metodo isin()
obj.isin(["b", "c"])

#Util para filtrar
mask = obj.isin(["b", "c"])             
obj[mask]

#Podemos asignar indices a un vector de valores de una Serie. La idea es que por medio de una 
#Serie o Array de valores unicos podamos asignar un indice a cada valor de una Serie. Seria como
#darle niveles a una variable categorica
to_match = pd.Series(["c", "a", "b", "b", "c", "a"])            
unique_vals = pd.Series(["c", "b", "a"])

indices = pd.Index(unique_vals).get_indexer(to_match)
indices

#En el caso de que queramos contar la frecuencia de aparicion de un valor en un DataFrame para 
#cada una de las columnas podemos hacer lo siguiente
data = pd.DataFrame({"Qu1": [1, 3, 4, 3, 4], 
                     "Qu2": [2, 3, 1, 2, 3],
                     "Qu3": [1, 5, 2, 4, 4]})
data

data["Qu1"].value_counts()                      #Contamos frecuencia  
data["Qu1"].value_counts().sort_index()         #Ordenamos por indice

#Para realizar esto mismo para todas las columnas nos ayudamos del metodo apply().
#Aqui los valores distintos se muestran en el index (columan de indice)
result = data.apply(pd.value_counts).fillna(0); result 

#Si aplicaramos el metodo .values_counts() directamente a un DataFrame nos entregaria 
#la frecuencia de aparicion de la combinacion de cada columna del DF
data = pd.DataFrame({"a": [1, 1, 1, 2, 2], "b": [0, 0, 1, 0, 0]}); data
data.value_counts()





#NOTAS
#----
#En numpy cuando creamos un vector nuevo en funcion al extracto de otro, este nuevo es una imagen y no una copia
#En Pandas cuando creamos un DF nuevo en funcion de otro por medio de loc[] o iloc[] creamos una copia



