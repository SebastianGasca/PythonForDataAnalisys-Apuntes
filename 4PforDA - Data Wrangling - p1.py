#--
#Hierarchical Indexing and Combing and Merging Dataset
#--
import pandas as pd
import numpy as np

# ---- # ---- # ----
# 8.1 Hierarchical Indexing
# Los indices jerarquicos son una caracteristica importante de pandas que permite tener multiples niveles 
# de indices en un eje (por filas o por columnas). Ej.
data = pd.Series(np.random.uniform(size=9), 
                 index=[["a", "a", "a", "b", "b", "c", "c", "d", "d"], 
                        [1, 2, 3, 1, 3, 1, 2, 2, 3]])

data        
data.index          #Tenemos un indice compuesto por tuplas.

# La selecciona por indices jerarquicos se da de la siguiente forma
data["b"]           #Todo lo de "b"
data["b":"c"]       #Todo lo de "b" y "c"
data[["b", "d"]]

# Podemos seleccionar un indice mas interno. Seleccionamos todo del indice externo con ":" y todo lo que 
# tenga el indice 2
data.loc[:,2]

# Los indices jerarquicos forman un importante rol en "reshaping data" y en "group-based operations". 
# Ej usando los metodos .unstack() y stack()
data
data.unstack()
data.unstack().stack()

# Podemos tener jerarquia en los indices tanto en filas como columnas en un DF
frame = pd.DataFrame(np.arange(12).reshape((4, 3)),
                     index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
                     columns=[["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]])

frame

# Podemos agregar nombres a cada nivel y ver el numero de niveles que posee un indice
frame.index.names = ["key1", "key2"]
frame.columns.names = ["state", "color"]
frame

frame.index.nlevels         

# Un "MultiIndex" puede ser creado por si mismo y entonces ser reutilizado
pd.MultiIndex.from_arrays([["Ohio", "Ohio", "Colorado"],
                          ["Green", "Red", "Green"]],
                          names=["state", "color"])




# ---- # ---- # ----
# 8.1.1 Reordering and Sorting Levels
# Podemos reordenar los niveles, por ejemplo, cambiando el indice "key1" por "key2"
frame.swaplevel("key1","key2")

# .sort_index() ordena la data "lexicographically" usando los niveles de los indices.
# Se puede usar un simple nivel o sun subconjunto de niveles para el orden. 
frame.sort_index(level=1)
frame.swaplevel("key1", "key2").sort_index(level=0)




# ---- # ---- # ----
# 8.1.2 Reordering and Sorting Levels
# Muchas estadisticas descriptivas y de resumenes en DataFrames o Series tienen una option de "level"
# donde se puede especificar el nivel que se quiere usar para agregar.

frame
frame.groupby(level="key2").sum()                       #Agrupamos y trabajamos sobre indice "key2" de filas
frame.groupby(level="color", axis="columns").sum()      #Agrupamos y trabajamos sobre indice "color" de columnas




# ---- # ---- # ----
# 8.1.3 Indexing with a DataFrame's columns
frame = pd.DataFrame({"a": range(7), 
                      "b": range(7, 0, -1),
                      "c": ["one", "one", "one", "two", "two","two", "two"],
                      "d": [0, 1, 2, 0, 1, 2, 3]})
frame

#En ocaciones queremos usar columnas como indices, .set_index() nos ayuda a esto
frame2 = frame.set_index(["c", "d"]); frame2

#Por defecto las columnas pasadas a indices son removidas, se puede omitir esto
frame.set_index(["c", "d"], drop=False)

#Al contrario de .set_index() tenemos .reset_index() haciendo que los indices pase a columnas
frame2.reset_index()




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 8.2 Combining and Merging Datasets
#Tenemos
# pandas.merge: Conecta las filas basados en uno o mas "keys". Es simplemente un join de SQL

# pandas.concat: Concadena o "stack" objetos a lo largo de un eje. Como un rbind() o cbind() 

# combine_first: Empalma data sobrepuesta para rellenar valores nulos en un objeto con valores del otro.




# ---- # ---- # ----
# 8.2.1 Database-Style DataFrame Joins
# Merge o "joins operations" combinan datasets por union entre filas usando uno o mas "keys"

df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "a", "b"],
                    "data1": pd.Series(range(7), dtype="Int64")})
df1

df2 = pd.DataFrame({"key": ["a", "b", "d"],
                    "data2": pd.Series(range(3), dtype="Int64")})
df2

# Tenemos el clasico .merge() que trabaja siendo un inner_join. 
# Si no especificamos que columnas usamos para unir, por defecto une las solapadas entre los dos datasets
pd.merge(df1, df2)
pd.merge(df1, df2, on="key")

# Si las columnas por la que vamos a unir los DFs son diferentes hay que especificarlas.
df3 = pd.DataFrame({"lkey": ["b", "b", "a", "c", "a", "a", "b"],
                    "data1": pd.Series(range(7), dtype="Int64")})

df4 = pd.DataFrame({"rkey": ["a", "b", "d"],
                    "data2": pd.Series(range(3), dtype="Int64")})

pd.merge(df3, df4, left_on="lkey", right_on="rkey")

# Como dijimos, por defecto .merge() trabaja como "inner join". Podemos cambiar su comportamiento
# especificando el tipo de join que queremos "left", "right" o "outer" que seria un full join
pd.merge(df1, df2, how="outer")
pd.merge(df3, df4, left_on="lkey", right_on="rkey", how="outer")

# El ejemplo anterior de join fue una relacion "muchos a uno". Si hacemos una relacion "muchos a muchos"
# tenemos el producto cartesiano de la union entre "keys". Ej.
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"],
                    "data1": pd.Series(range(6), dtype="Int64")})
df1

df2 = pd.DataFrame({"key": ["a", "b", "a", "b", "d"],
                    "data2": pd.Series(range(5), dtype="Int64")})
df2

# En df1 el "key" b con valor en "data1" 0 se use a ambas "keys" b del set de datos "df2".
pd.merge(df1,df2, on ="key", how="left")            

# Podemos unir DFs por multiples "keys" por medio de una lista de nombres
# La union por multiples columnas debe ser pensada como que cada combinacion de columnas es una llave unica
left = pd.DataFrame({"key1": ["foo", "foo", "bar"],
                     "key2": ["one", "two", "one"],
                     "lval": pd.Series([1, 2, 3], dtype='Int64')})
left

right = pd.DataFrame({"key1": ["foo", "foo", "bar", "bar"],
                      "key2": ["one", "one", "one", "two"],
                      "rval": pd.Series([4, 5, 6, 7], dtype='Int64')})
right

pd.merge(left, right, on=["key1", "key2"], how="inner")
pd.merge(left, right, on=["key1", "key2"], how="outer")


# Un ultimo problema a considerar en las "merge operations" es el tratamiento de los nombres de columnas
# iguales.
pd.merge(left, right, on="key1")

# A pesar de que podemos cambiar los nombres manualmente, .merge() posee un atributo "suffixes" para
# cambiar los nombres
pd.merge(left, right, on="key1", suffixes=("_left", "_right"))




# ---- # ---- # ----
# 8.2.2 Merging on Index
# En algunos casos, la columna que queremos usar para unir un DF con otro, es su indice 
left1 = pd.DataFrame({"key": ["a", "b", "a", "a", "b", "c"],
                      "value": pd.Series(range(6), dtype="Int64")})
left1

right1 = pd.DataFrame({"group_val": [3.5, 7]}, index=["a", "b"])
right1

pd.merge(left1, right1, left_on="key", right_index=True)
# Observar que el DF resultante viene con el indice del DF left1 ordenado por right1. 
# En los casos que vimos anteriormente el indice no se conservaba.

# Con indices jerarquicos las cosas son de la siguiente forma.
lefth = pd.DataFrame({"key1": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada"],
                      "key2": [2000, 2001, 2002, 2001, 2002],
                      "data": pd.Series(range(5), dtype="Int64")})
lefth

righth_index = pd.MultiIndex.from_arrays([
    ["Nevada", "Nevada", "Ohio", "Ohio", "Ohio", "Ohio"],
    [2001, 2000, 2000, 2000, 2001, 2002]])
righth = pd.DataFrame({"event1": pd.Series([0, 2, 4, 6, 8, 10], dtype="Int64", index=righth_index),
                       "event2": pd.Series([1, 3, 5, 7, 9, 11], dtype="Int64", index=righth_index)})
righth

pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True)
pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True, how="outer")

# Usar los indices en ambos DFs para ser unidos igual es una opcion
left2 = pd.DataFrame([[1., 2.], [3., 4.], [5., 6.]],
                     index=["a", "c", "e"],
                     columns=["Ohio", "Nevada"]).astype("Int64")
left2

right2 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]],
                      index=["b", "c", "d", "e"],
                      columns=["Missouri", "Alabama"]).astype("Int64")
right2

pd.merge(left2, right2, left_index=True, right_index=True, how="outer")

# El metodo llamado ".join" une los DFs tomando en consideracion los indices. Por defecto uso left_join
left2.join(right2, how="outer")       

# Podemos unirnos al indice de otro DF por medio de una columna de nuestro DF principal por el atributo "on"
left1.join(right1, on="key")




# ---- # ---- # ----
# 8.2.3 Concatenating Along an Axis
#Otro tipo de metodo de operaciones de combinacion es "concatenation o stacking". 
#Por numpy la concadenacion sigue la siguiente forma
arr = np.arange(12).reshape((3, 4)); arr

np.concatenate([arr,arr])           #por defecto concadenamos por filas
np.concatenate([arr,arr], axis = 1) #asignamos concadenar por columnas

#En el contexto de Pandas el tener etiquetas (en filas y columnas) tenemos 
#alguna  preocupaciones adicionales

s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64"); s1
s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64"); s2
s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64"); s3

#Al igual que en Numpy, por defecto concadenamos por filas
pd.concat([s1, s2, s3])             

#Si concadenamos por columnas y los indices de los objetos no coinciden 
#ninguna fila se unira a la otra, solo se agregaran como una fila nueva con NAs
pd.concat([s1, s2, s3], axis=1)     

#En caso de que existan indices que coincidan entre los objetos estos se uniran
s4 = s4 = pd.concat([s1, s3])
pd.concat([s1, s4], axis="columns")

#Podemos especificar que solo quede donde los indices coincidan con join="inner"
pd.concat([s1, s4], axis="columns", join="inner")

#Podemos al momento de concadenar definir indices jerarquicos para identificar 
#los objetos unidos (es "como" ponerle nombres a los objetos unidos)

#Por filas
result = pd.concat([s1, s1, s3], keys=["one", "two", "three"]); result
result.unstack()

#Por columnas
pd.concat([s1, s2, s3], axis="columns", keys=["one", "two", "three"])

#La misma logica opera cuando trabajamos con DataFrames
df1 = pd.DataFrame(np.arange(6).reshape(3, 2), index=["a", "b", "c"],
                   columns=["one", "two"]); df1

df2 = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=["a", "c"],
                   columns=["three", "four"]); df2

pd.concat([df1, df2], axis="columns", keys=["level1", "level2"])

#Si pasamos un diccionario es una forma alternativa de usar el parametro "key="
pd.concat({"level1": df1, "level2": df2}, axis="columns")

#Podemos ponerle nombres a los niveles del eje (columnas o filas) que estamos usando 
#con "names=". 
df = pd.concat([df1, df2], axis="columns", keys=["level1", "level2"], 
          names=["upper", "lower"])

#Como ultima cosa, en caso de que los indices de lo objetos que vamos a usar no 
#nos son de importancia podemos poner "ignore_index = True". 
# Con esto no conservamos los indices y creamos uno nuevo para el nuevo objeto
df1 = pd.DataFrame(np.random.standard_normal((3, 4)),
                   columns=["a", "b", "c", "d"])

df2 = pd.DataFrame(np.random.standard_normal((2, 3)),
                   columns=["b", "d", "a"])

pd.concat([df1, df2], ignore_index=True)




# ---- # ---- # ----
# 8.2.4 Combing Data with Overlap
# Hay otro tipo de combinacion de datos que no son "merge"(clasico join en sql), ni
# concadenacion (rbind o cbind en R). 

# Veamos un ejemplo.

# El metodo "where" de Numpy realiza un expresion if-else 
a = pd.Series([np.nan, 2.5, 0.0, 3.5, 4.5, np.nan],
              index=["f", "e", "d", "c", "b", "a"])
a

b = pd.Series([0., np.nan, 2., np.nan, np.nan, 5.],
              index=["a", "b", "c", "d", "e", "f"])
b

np.where(pd.isna(a), b, a)

# Lo anterior es "si en el DF 'a' es nulo, entonces coloca b, sino a"
# numpy.where no verifica que los indices coincidan. Vimos que el primer
# elemento del DF 'a' siendo nulo con indice f, fue rellenado por 0.0 del DF b 
# con indice b 

# Si queremos hacer que el "relleno" coincida con los indice tenemos
a.combine_first(b)

# Si lo hacemos con DataFrames se va rellenando columna por columna
df1 = pd.DataFrame({"a": [1., np.nan, 5., np.nan],
                    "b": [np.nan, 2., np.nan, 6.],
                    "c": range(2, 18, 4)})

df2 = pd.DataFrame({"a": [5., 4., np.nan, 3., 7.],
                    "b": [np.nan, 3., 4., 6., 8.]})

df1.combine_first(df2)















