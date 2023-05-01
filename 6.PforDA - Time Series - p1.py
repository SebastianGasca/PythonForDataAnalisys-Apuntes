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











