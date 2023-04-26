import numpy as np

#Creamos serie
my_arr = np.arange(100)
my_arr = np.arange(False)

#Multiplicamos
my_arr * 2

# ---- # ---- # ----
# 1.1 Intro
#Creamos un array (puede tener multiples dimensiones)
data = np.array([[1,2,3], [4,5,6]]); data
type(data) 

#Aplicamos operaciones a un array
data + data
data * 10 

#En un array todos los elementos deben ser de la misma clase
data.dtype #tipo de dato


# ---- # ---- # ----
# 1.2 Creating ndarrays

#Creamos un array 
arr1 = np.array([np.arange(5), np.arange(5)]) ; arr1

#Revisamos dimensiones y el tipo de datos que alberga
arr1.ndim
arr1.shape

#Revisamos tipo de datos que componen un array 
arr1.dtype

#Creamos arrays especiales 
np.ones(5)

np.empty((3,3))

np.zeros((2,3,3)) 

np.full((4,3,2), 2) 

#La funcion arange() de numpy es un simil a la funcion range() nativa de python
np.arange(3)


# ---- # ---- # ----
# 1.3 Data Types for Ndarrays

#Definimos el tipo de de datos de un array
#Para mas informacion de los tipos utiles ver Tabla 4.2

arr1 = np.array([1,2,3], dtype=np.float64) ; arr1.dtype
arr2 = np.array([1,2,3], dtype=np.int32) ; arr2.dtype

#Tenemos los tipos por ejemplo int32 y uint32, el primero llamado singed inter 
#representa a los entero negativos y positivos, en cambio unsiged inter solo
#representa a los enteros positivos

arr1 =  np.array([1,2,3], dtype=np.uint32) ; arr1.dtype
arr2 = np.array([-1,-2,1,2], dtype=np.int32) ; arr2.dtype

#Podemos cambiar el tipo de datos de un array. 
# int32 a float64
arr1 = np.array([1,2,3], dtype=np.int32)
arr1 = arr1.astype(np.float64); arr1.dtype

# string a float32
arr1 = np.array(["1.25", "-9.6", "42"], dtype=np.string_); arr1.dtype
arr1.astype(np.float32)


#Podemos usar el tipo de datos de otro array
int_array = np.arange(10)
float_array = np.array([.22, .270, .357, .380, .44, .50], dtype=np.float64)

int_array = int_array.astype(float_array.dtype); int_array.dtype


# ---- # ---- # ----
# 1.4 Arithmetic with Numpy Arrays
arr = np.array([[1., 2., 3.], [4., 5., 6.]])

#Podemos sumar, restar, multiplicar, dividir, elevar al cuadrado y otros a un ndarray
arr - 10
arr / 2
arr ** 2
arr - arr

#Podemos comparar dos array de las mismas dimensiones
arr1 = np.array([[2,4,6], [1,5,1]])
arr > arr1

arr1 = np.array( [5,1,2] ) ; arr1
arr > arr2

arr2 = np.array( [[5], [1]] ) ; arr2
arr > arr2


# ---- # ---- # ----
# 1.5 Basic Indexing and Slicing
arr = np.arange(10)

#Accedemos a los valores de un array
arr[5]
arr[5:8]

#Podemos asignar valores
arr[5:8] = 12 ; arr

#Un array producto de un pedazo de otro array SOLO UNA VISUALIZACION del array fuente
#si desplegamos el array fuente tambien pose la modificacion
arr1 = arr[5:8] ; arr1
arr1[1] = 12345
arr 

#hay que usar el metodo .copy (en pandas igual pasa lo mismo)
arr1 = arr[5:8].copy ; arr1
arr1[1] = 12345
arr

#Accedemos a los valores de un array de 2d. 
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

arr2d[0][2] #forma 1
arr2d[0, 2] #forma 2

arr2d[:, 1:] #todas las filas, solo las 2 ultimas columnas
arr2d[ :2, 1: ] #las dos primeras filas, desde la segunda columna

# ---- # ---- # ----
# 1.6 Boolean Indexing
names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])
data = np.array([[4, 7], [0, 2], [-5, 6], [0, 0], [1, 2],[-12, -4], [3, 4]])

#por medio de un array boleano podemos filtrar datos
names == "Bob"                                  # array boleano 
data[[True,False,False,False,False,False,True]] # filtro por arrray boleano

data[names == "Bob"]                            # filtro por array boleano creado a partir de otro array
data[names == "Bob", 1:]    # solo segunda columna
data[names == "Bob", 1]     # solo primera columna

#podemos invertir el igual por un distinto 
data[names != "Bob"]        # !=
data[~(names == "Bob")]     # ~()

#los operados "|"" y "&" son "o" e "y" respectivamente
data[(names == "Bob") | (names == "Will")]      

#podemos asignar valores por medio de un Bolean Indexing
data < 0
data[data < 0] = 0 ; data

data[names != "Joe"] = 7 ; data

# ---- # ---- # ----
# 1.7 Fancy Indexing

#Podemos acceder a los elementos (ej. filas o columnas enteras) 
#de un array por medio de indices
arr = np.zeros((8, 4)) ; arr
for i in range(8):
    arr[i] = i
arr

arr[[1,3,5]]    #filas
arr[:, [2,3]]   #columnas
arr[[-5,-3,-1]] #con indices negativos

#podemos seleccionar combinaciones particulares (x,y)
arr[[1,2], [1,2]]           #se selecciona la cordenada 1,1 y 1,2
arr[[1,2,3], [1,2,2]]       #se seleccionada la cordenada 1,1 ; 2,2 ; 3,2


#podemos seleccionar segmentos de un narray (matrices mas pequeñas)
arr = np.arange(32).reshape((8, 4)); arr
arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]] 


# ---- # ---- # ----
# 1.8 Transposing Arrays

#Podemos rehacer la forma de un array 
arr = np.arange(12).reshape(3,4); arr    #de un vector de largo 9 lo reordenamos a una matriz de 3x3

#Podemos Trasponer una matriz
arr.T


# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----


# ---- # ---- # ----
# 2. Pseudorandom Number Generation

#Generamos narray de numeros aleatorios con distribucion normal
samples = np.random.standard_normal((2,3)) ; samples


#Los numeros aleatorios no son tan aleatorios. Usamos una "semilla" para indicar un estado de aleatoriedad 
#En el siguiente ejemplo seleccionamos una semilla y cada vez luego de ella nuestro programa generara 
#los mismos numeros aleatorios

rng = np.random.default_rng(seed=1234)
rng.standard_normal((2,2))              #(0,0) es -1.6 siempre luego de la semilla 1234
rng.standard_normal((2,2))              #(0,0) es 0.86 siempre luego de la semilla 1234 y la linea anterior


# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----


# ---- # ---- # ----
# 3. Universal Functions: Fast Element-Wise Array Functions
# las universal function o ufunc son funciones para realizar operaciones vectoriales sobre los elementos array

arr = np.arange(10)

# hay funciones que requieren solo de un vector
np.sqrt(arr)        #funcion cuadratica sobre los elementos del vector
np.exp(arr)         #funcion expotencial sobre los elementos del vector


# hay funciones que requieren de dos vectores
x = rng.standard_normal(8) ; x
y = rng.standard_normal(8) ; y

np.maximum(x, y)    #verificamos el maximo para cada par de elementos

# hay funciones que entregan de output dos vectores
arr = rng.standard_normal(7) * 5 ; arr

remainder, whole_part = np.modf(arr)    
remainder, whole_part                   #entrega una tupla de la parte decimal y entera de un numero tipo float

#VER TABLA 4.4 si se quieren conocer mas ufunc


# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----


# ---- # ---- # ----
# 4. Array-Oriented Programming with Arrays
#Es la practica de aplicar metodos a los arrays, que en cualquier otro caso se usarian loops. A esto le llamamos vectorizacion

#Entendamos primero el metodo .meshgrid()
nx, ny = (3, 2); 
x = np.linspace(0, 1, nx); x    #array que va del 0 al 1 en 3 pasos
y = np.linspace(0, 1, ny); y    #aaray que va del 0 al 1 en 2 pasos
xv, yv = np.meshgrid(x, y)      #genera 2 matrices que poseen las combinaciones entre dos vectores

#Veamos que podemos sacar la raiz de la suma cuadratica entre dos matrices gracias a la vectorizacion. 
points = np.arange(-5, 5, 0.01); points     #array que va del -5 al 5 
xs, ys = np.meshgrid(points, points)
z = np.sqrt(xs ** 2 + ys ** 2)

# ---- # ---- # ----
# 4.1 Expressing Conditional Logic as Array Operations

#Tenemos la funcion np.where() en numpy para seleccionar por condicion. Es como un if_else() en R. 
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])

result = np.where(cond, xarr, yarr); result     #dada la condicion, se da xarr o en caso contrario yarr

#Notar que no es necesario remplazar un vector por otro vector, el remplazo puede ser un escalar
arr = rng.standard_normal((4, 4))
np.where(arr > 0, 2, -2)                        #dado algun elemento mayor a 0 se asigna 2, en caso contrario -2

# ---- # ---- # ----
# 4.1 Mathematical and Statistical Methods

#Diferentes funciones matematicas tenemos como metodos para los arrays. 
arr = rng.standard_normal((5, 4)); arr

arr.mean()          #el calculo es a total valores matriz
arr.sum()           
arr.argmax()        #indice del maximo valor

#Si asignamos el parametros de "axis =" definimos el eje por el cual realizar el calculo
arr.mean(axis=1)    #a traves de las columnas
arr.sum(axis=0)     #a traves de las filas 

np.arange(9).reshape(3,3)
np.arange(9).reshape(3,3).sum(axis=1)   #a traves de las columnas es de derecha a izquierda
np.arange(9).reshape(3,3).sum(axis=0)   #a traves de las filas es de arriba hacia abajo 


#Otros metodos como .cumsum() no son outputs agregados como .sum() (que solo entrega un valor)
arr.cumsum()
np.arange(9).reshape(3,3).cumsum()
np.arange(9).reshape(3,3).cumsum(axis=1)    #suma acumulada a traves de las columnas
np.arange(9).reshape(3,3).cumsum(axis=0)    #suma acumulada a traves de las filas

# ---- # ---- # ----
# 4.2 Methods for Boolean Arrays
#Los valores True son considerados como 1 y False como ceros, por ende podemos

arr = rng.standard_normal(100)
(arr > 0).sum()                             #contamos los valores positivos

#Metodos como .any() o .all() nos ayuda a consultar vectores booleanos sobre si alguno es True
bools = np.array([False, False, True, False])
bools.any()
bools.all()

# ---- # ---- # ----
# 4.3 Sorting
# Con el metodo .sort() podemos ordenar un array. 
# Este metodo deja ordenado el array sin tener que guardarlo en una variable nueva 

arr = rng.standard_normal(6); arr
arr.sort()
arr                                     #revisamos que el array quedo ordenado

arr = rng.standard_normal((3, 3)); arr
arr.sort(axis=1); arr                   #ordenamos por columnas   
arr.sort(axis=0); arr                   #luego ordenamos por fila


# Ademas de modificar el array "in place", podemos hacer una copia de la variable con la funcion np.sort()
arr2 = np.array([5, -10, 7, 1, 0, -3]); arr2
sorted_arr2 = np.sort(arr2); sorted_arr2
arr2                                    #revisamos que arr2 no fue modificado porque sorted_arr2 es copia y no referencia de arr2

# ---- # ---- # ----
# 4.4 Unique and Other Set Logic
#Podemos verificar los valores unico de un array con la funcion de numpy np.unique()
names = np.array(["Bob", "Will", "Joe", "Bob", "Will", "Joe", "Joe"])
np.unique(names)

nts = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
np.unique(nts)

#Podemos verificar si un conjunto de valores se encuentran en un array con la funcion np.in1d()
values = np.array([6, 0, 0, 3, 2, 5, 6])
np.in1d(values, [2, 3, 6])

#Podemos verificar que elementos comparten dos arrays con la funcion np.intersect1d()
np.intersect1d(values, [6,0,8])

#Podemos verificar que elementos estan en en el primer array pero no en el segundo con np.setdiff1d()
np.setdiff1d(values, [6,0,8])

#Podemos unir (mostrando los unicos y de manera ordenada) ambos array con la funcion np.union1d()
np.union1d(values, [6,0,8])














