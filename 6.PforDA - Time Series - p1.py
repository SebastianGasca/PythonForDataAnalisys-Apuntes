#--

#--
import pandas as pd
import numpy as np

# ---- # ---- # ----
# 11 Time Series

# La series de tiempo pueden ser de "frecuencia fija" o "frecuencia irregular"
# las primera indican que  los intervalos de tiempos entre puntos es constante, la 
# segunda que los intervalos de tiempos entre puntos no es constante. 

# Algunos conceptos: 
# Timestamps = instante especifico del tiempo
# Fixed periods = como todo el mes de enero 2017, o todo el año 2022
# Intervals of time = indicado por una marca de tiempo de inicio y finalización.


# ---- # ---- # ----
# 11.1 Date and Time Data Types and Tools
# Python trae consigo librerias para poder trabajar con fechas: datetime, time y calendar

from datetime import datetime
now = datetime.now(); now
type(now)

#Podemos acceder al año, mes o día de un datetime.datetime object
now.year
now.month
now.day

#Podemos operar entre fechas. El resultado es un objeto datetime.timedelta. 
delta = datetime(2011,1,7) - datetime(2008, 6, 24, 8, 15); delta

delta.days                      #Accedemos a los resulados de la operacion 
delta.seconds   

#Podemos utilizar un objeto datetime.timedelta para operar sobre un objeto datetime.datetime 
from datetime import timedelta
start = datetime(2011, 1, 7)
start + timedelta(12)           #Se obsera que timedelta(12) se referencia por defecto a dias


# ---- # ---- # ----
# 11.1.1 Converting Between String and Datetime
# Podemos convertir un datetime object o un timestamps (objecto fecha de pandas) a un string por medio
# del metodo de datetime.strftime()  o la funcion str()

stamp = datetime(2011, 1, 3)

stamp.strftime("%Y-%m-%d")      #por medio del metodo .strftime() 
str(stamp)                      #por medio de la funcion str()


# De la forma contraria, podemos pasar de string a dates usando la funcino de datatime.strptime()
value = "2011-01-03"
datetime.strptime(value, "%Y-%m-%d")

datestrs = ["7/6/2011", "8/6/2011"]
[datetime.strptime(x, "%m/%d/%Y") for x in datestrs]


# Pandas esta orientado a trabajar con arrays de fechas, por lo que el metodo pandas.to_datetime()
# es conveniente para pasar arrays de string a fechas. 
datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]
dates =  pd.to_datetime(datestrs); dates

[type(datetime.strftime(i, "%Y-%m-%d")) for i in dates]




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 11.2 Time Series Basics
# Un tipo basico de serie de tiempo en pandas es una Serie indexada por peridos de tiempo.

#Creamos una lista de datatime objects y la utilizaremos como indice para una pd.Series()
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5),
         datetime(2011, 1, 7), datetime(2011, 1, 8),
         datetime(2011, 1, 10), datetime(2011, 1, 12)]

ts = pd.Series(np.random.standard_normal(6), index=dates); ts

#Esa serie de datetime objects ahora, en el indice de un pd.Series, es un DatetimeIndex
ts.index

#Como cualquier otra Serie las operaciones aritmeticas se hacen por la union entre indices.
ts + ts[::2]        #Recordar que ts[::2] indica seleccion cada dos elementos. 

#Pandas almacena los timestamps como datos de tipo "datetime64" con resolucion de nanosegundo 
ts.index.dtype

#Los valores escalares de una DatetimeIndex son objectos "Timestamps" de Pandas
stamp = ts.index[0]; stamp




# ---- # ---- # ----
# 11.2.1 Indexing, Selection, Subsetting
# Las Series de tiempos se comportan como cualquier otra Serie cuando tu estas "indexing and selecting" 
# datos basados en etiquetas 
stamp = ts.index[2]; stamp      #Usando una etiqueta del indice, version 1             
ts[stamp]

ts["2011-01-10"]                #Usando una etiqueta del indice, version 2


#Para series de tiempo mas largas, podemos utiilzar un año, o un año y un mes como etiqueta de filtro 
longer_ts = pd.Series(np.random.standard_normal(1000), 
                      index=pd.date_range("2000-01-01", periods=1000)); longer_ts

longer_ts["2001"]               #Solo un año
longer_ts["2001-05"]            #Un año un mes


#Los Datetime Objetos de Python tambien funcionan como etiquetas para filtrar
ts
ts[datetime(2011,1,7)]

#Como las series de tiempo son cronologicas, podemos hacer filtros por rangos. Ademas, no es necesario
#que la fecha ingresada en el rango exista.
ts
ts["2011-01-06":"2011-01-10"]

#NOTA: 
# Al igual que en los arrays de Numpy, las Series obtenidas por "slicing" no son copias (solo "views"), 
# sino que siguen siendo referenciadas a la Serie de origen

#El metodo .truncate() nos divide en dos la Serie dada una fecha entregada
ts.truncate(after="2011-01-09")

#Tdo lo anterior se cumple con los DataFrames 
dates = pd.date_range("2000-01-01", periods=100, freq="W-WED"); 
long_df = pd.DataFrame(np.random.standard_normal((100, 4)),
                       index=dates,
                       columns=["Colorado", "Texas","New York", "Ohio"])

long_df.loc["2001-05"]




# ---- # ---- # ----
# 11.2.2 Time Series with Duplicate Indices
#En algunas aplicaciones, hay multiples observaciones con el mismo instante de tiempo
dates = pd.DatetimeIndex(["2000-01-01", "2000-01-02", "2000-01-02", "2000-01-02", "2000-01-03"]); dates
dup_ts = pd.Series(np.arange(5), index=dates)

#Podemos comprobar si los indices son unicos con el metodo para indices .is_unique
dup_ts.index.is_unique

#Si los indices no son unicos, la seleccion de elementos por indices ahora podra retornarnos
#valores singulares o multiples

dup_ts["2000-01-03"]  # not duplicated
dup_ts["2000-01-02"]  # duplicated

#Si nos conviene podemos utilizar .groupby() para agrupar los indices duplicados. Con ayuda
#del parametro "level=0" decimos que queremos agrupar por el indice
grouped = dup_ts.groupby(level=0)
grouped.mean()
grouped.count()




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 11.3 Date Ranges, Frequencies, and Shifting

# ---- # ---- # ----
# 11.3.1 Generating Date Ranges
# Como hemos visto .data_ranges() puede generar un DateTimeIndex de un determinado largo 
# acorde a una determinada frecuencia

# En el siguiente ejmpleo generamos un DateTimeIndex desde "2012-04-01" a "2012-06-01" con 
# frecuencia diaria (que es la por defecto)
index = pd.date_range("2012-04-01", "2012-06-01"); index

# Si solo ponemos una fecha podemos agregar la cantidad de periodos consecutivos a ella con 
# "periods" 
pd.date_range(start = "2012-04-01", periods=20)     #Usamos "start"
pd.date_range(end = "2012-04-01", periods=20)       #Usamos "end"

#Podemos moficiar la frecuencia de los Timestamp generados. Por ejemplo en vez de que fuera
#diario podria ser el ultimo dia laboral del mes (Business end of month -> BM)
pd.date_range("2000-01-01", "2000-12-01", freq="BM")


#VER LA TABLA 11.4 con las abrevaciones para cada frecuencia disponible


#Por defecto .data_range() conserva el tiempo (si es que lo trae) del comienzo o el final
#del Timestamp. Pero podemos normalizarlo a que posea el medio dia. 

pd.date_range("2012-05-02 12:56:31","2012-10-02 11:50:27")          #DataTimeIndex conserva 12:56:31
pd.date_range("2012-05-02 12:56:31", periods=5)             


pd.date_range("2012-05-02 12:56:31", periods=5, normalize=True)     #DateTimeIndex Noramlizado


# ---- # ---- # ----
# 11.3.2 Frequencies and Date Offsets
# Las frecuencias en Pandas son compuestas por un "base frecuency" y "multiplier".

# Las "base frecuency" son las referencias tipicas de string como "M" para frecuencia Mensual 
# o "H" para frecuencia por hora. Para cada "base frecuency" hay un objeto referido como "date offset" 

from pandas.tseries.offsets import Hour, Minute

hour = Hour(); hour                         #"date offset" de Hora 
four_hours = Hour(4); four_hours            #"date offset" de 4 Horas                 

Hour(2) + Minute(30)                        #Aritmetica con "date offset"


#En verdad pocas veces usamos los "data offset", es mas comun usar los formatos string como "H" o "4H" 
pd.date_range("2000-01-01", "2000-01-03 23:59", freq="4H")      #freq de cada 4 horas
pd.date_range("2000-01-01", periods=10, freq="1h30min")         #frea de 1h y 30 min

#Una frecuencia muy usada es la semana de cada mes, esta frecuencia queda sujeta al
#string alias de "WOM" (week of months). 
#En el siguiente ejemplo tenemos WOM-3FI que indica el tercer viernes de cada mes
monthly_dates = pd.date_range("2012-01-01", "2012-09-01", freq="WOM-3FRI"); monthly_dates

# ---- # ---- # ----
# 11.3.3 Shifting (Leading and Lagging) Data
# Nos referimos a "Shifting" cuando movemos los datos hacia adelante o hacia atras a traves
# del tiempo. 
# Existe el metodo .shifts() nos permite mover los datos hacia adelante o hacia atras sin
# modificar el indice. Obsevar que al mover los datos introducimos NAs 

ts = pd.Series(np.random.standard_normal(4),
               index=pd.date_range("2000-01-01", periods=4, freq="M"))

ts
ts.shift(2)                         #movemos hacia adelante los datos dos momentos en el tiempo
ts.shift(-2)                        #movemos hacia atras los datos un momento en el tiempo 

#Un comun uso de .shift es calcular la variacion porcentual en el tiempo.
ts / ts.shift(1) - 1

#Dado que el indice no se modifica algunos datos son descartados (quedan indices con valores NAs)
#Por lo tanto si la frecuencia es conocida, esta puede ser pasada para que no solo se muevan los 
#datos sino tambien los indices

ts
ts.shift(2, freq="M")               #Desplazamos los indices sobre una frecuencia Mensual (ej: 31 de enero a 31 de marzo) 
ts.shift(3, freq="D")               #Desplazamos los indices sobre una frecuencia Diaria  (ej: 31 de enero al 3 de febrero)
ts.shift(1, freq="90T")             #Desplazamos los indices sobre frecuencia de 90T (min)


#Shifting dates with offsets
#(Recordar que los "date offsets" son los objetos asociados a los "string alias" que usamos para definir 
# una freq)
#Los "date offsets" de Pandas pueden ser usados con objetos datetime or timestamp

from pandas.tseries.offsets import Day, MonthEnd
now = datetime(2011, 11, 17)
now + 3 * Day()

#Si tu sumas un "anchored offset" como MonthEnd(), el primer incremento llevara a la fecha
#a la siguiente fecha acorde a la regla de la frecuencia

now + MonthEnd()
now + MonthEnd(2)
now + MonthEnd(-1)

#Los "anchored offset" pueden ser aplicados a una fecha por medio de sus metodos .rollfoward o .rollback

offset = MonthEnd()
offset.rollforward(now)
offset.rollback(now)

#Un uso creativo para el uso de un "anchored offset" y sus metodos vistos, es aplicandolo con un .groupby()
ts = pd.Series(np.random.standard_normal(20), index=pd.date_range("2000-01-15", periods=20, freq="4D")); ts
ts.groupby(MonthEnd().rollforward).mean()

#Aunque lo anterior puede ser remplazado por un .resample() (aun no visto)
ts.resample("M").mean()




