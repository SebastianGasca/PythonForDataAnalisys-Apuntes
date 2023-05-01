import numpy as np
import pandas as pd

# ---- # ---- # ----
# 2.3 Apply: General split-apply-combine
# El metodo de uso mas general de groupby es .apply(). Este metodo trabaja sobre el DF agrupado
# e invoca una funcion a cada grupo y trata de concadenar cada pieza con la funcion aplicada. 

tips = pd.read_csv("tips.csv", sep=None); tips

tips.rename(columns={"\ufefftotal_bill":"total_bill"}, inplace=True)
tips["tip_pct"] = tips["tip"] / tips["total_bill"]

# Veamos un ejemplo, en donde aplicaremos la funcion top, que retorna los 5 primeros 
# valores mas altos para una columna dada, en este caso "tipo_pct"
def top(df, n=5, column="tip_pct"):
    return df.sort_values(column, ascending=False)[:n]

# Aplicaremos "top" en el DF agrupado por "smoker"
tips.groupby("smoker").apply(top)       #Los fumadores entregan mejores % de propinas?

# Podemos cambiar los parametros de la funcion entregada en .apply() luego de pasar
# el nombre de la funcion.
tips.groupby(["smoker","day"]).apply(top, n=1, column = "total_bill")

# Sacar el maximo provecho de .apply() es cosa de creatividad. Por ejemplo:
#op1
result = tips.groupby("smoker")["tip_pct"].describe(); result
result.unstack()

#op2
def f(group): return group.describe()
tips.groupby("smoker")["tip_pct"].apply(f)




# ---- # ---- # ----
# 2.3.1 Suppressing the Group Keys
# Con "group_keys = False" podemos desactivar el comportamiento por defecto de dejar 
# las combinaciones de llaves usadas para agrupar los DF como indices. 

tips.groupby("smoker").apply(top)
tips.groupby("smoker", group_keys=False).apply(top)

# Habiamos visto antes el atributo "as_index", pero este sirve cuando estamos usando .agg()
# ya que ahí estamos aplicando funcions de agregacion, en cambio con apply estamos usando
# funciones sobre trozos del DF

tips.groupby("smoker").agg("mean")
tips.groupby("smoker", as_index=False).agg("mean")




# ---- # ---- # ----
# 2.3.2 Quantile and Bucket Analysis
# Como habiamos visto, tenemos las funciones pd.cut() o pd.qcut() para segmentar series
frame = pd.DataFrame({"data1": np.random.standard_normal(1000),
                      "data2": np.random.standard_normal(1000)})
quartiles = pd.cut(frame["data1"],4); quartiles.head(5)
isinstance(quartiles.values, pd.Categorical)

# El objeto categorico entregado puede ser usado para generar grupos 
grouped = frame.groupby(quartiles)

def get_stats(group):
    return pd.DataFrame({"min": group.min(), "max": group.max(), 
                         "count": group.count(), "mean": group.mean()})
grouped.apply(get_stats)

#Tener en cuenta que un resultado parecido puede ser por medio de 
r1 = grouped.agg(["min","max","mean"]); r1
r1.stack(level=0)




# ---- # ---- # ----
# 2.3.3 Example: Filling Missing Values with Group-Specific Values
# Cuando tratamos con NAs, en algunos casos los eliminamos (dropna) y en otros los rellenamos (fillna)
# Es util rellenar los NAs en funcion al comportamiento de un grupo 

states = ["Ohio", "New York", "Vermont", "Florida",
          "Oregon", "Nevada", "California", "Idaho"]

group_key = ["East", "East", "East", "East",
             "West", "West", "West", "West"]

data = pd.Series(np.random.standard_normal(8), index=states); data
data[["Vermont", "Nevada", "Idaho"]] = np.nan; data

data.groupby(group_key).size()          
data.groupby(group_key).count()
data.groupby(group_key).mean()

# Vamos a rellenar los NAs en funcion a la media de cada region East y West
def fill_mean(group): return group.fillna(group.mean())
data.groupby(group_key).apply(fill_mean)

# Como dijimos antes, los objetos agrupados poseen identificador de name y group
# para acceder a su nombre y su contenido. Podemos asignar entonces un valor 
# predefindo 

fill_values = {"East": 0.5, "West": -1}
def fill_func(group): return group.fillna(fill_values[group.name])
data.groupby(group_key, group_keys=True).apply(fill_func)




# ---- # ---- # ----
# 2.3.4 Example: Filling Missing Values with Group-Specific Values
# Supongamos que queremos hacer un muestreo aleatorio de un conjunto grande datos.
# Hay diferentes formas de hacer esto, aca mostramos uno. Usaremos de ejemplo el 
# robo aleatorio en un mazo de cartas  

#Consturimos el mazo
suits = ["H", "S", "C", "D"]  # Hearts, Spades, Clubs, Diamonds
base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]; 
cards = []
for suit in suits:
    print(suit)
    cards.extend(str(num) + suit for num in base_names)

card_val = (list(range(1, 11)) + [10] * 3) * 4; card_val
deck = pd.Series(card_val, index=cards); deck

#Definimos la funcion de robo aleatorio
def draw(deck, n=5): return deck.sample(n)
draw(deck)

#Supongamos que queremos obtener dos carta aleatorios para cada pinta, para esto
#creamos una funcion que nos retorne el ultimo elemento de un .str. Recordar
#que cuando aplicamos una funcion como metodo para agrupar, la funcion opera sobre
#los indices del DFs

def get_suit(card):
   # last letter is suit
   return card[-1]

deck.groupby(get_suit).apply(draw, n=2)

#Otra forma mas "facil de ver" como lo anterior funciona es la siguiente
deck.index.str[-1]                                  #Vector con las pintas
deck.groupby(deck.index.str[-1]).apply(draw, n=2)   #Agrupamos por las pintas.





# ---- # ---- # ----
# 2.3.5 Example: Group Weighted Average and Correlation
# Es util, bajo el paradigma de groupby las operaciones entre columnas de un DFs or dos Series
# Como ejemplo calcularemos el promedio ponderado de una columna A por una B

df = pd.DataFrame({"category": ["a", "a", "a", "a",
                                "b", "b", "b", "b"],
                    "data": np.random.standard_normal(8),
                    "weights": np.random.uniform(size=8)})

df
grouped = df.groupby("category")

#Aplicamos el promedio ponderado utilizando columnas especificas de nuestro DF
def get_wavg(group): return np.average(group["data"], weights=group["weights"])
grouped.apply(get_wavg)

#Es util conservar nuestro DF, por lo que podemos agregar como columna el calculo
def get_wavg(group): 
    group["promedio_ponderado"] = np.average(group["data"], weights=group["weights"])
    return group

grouped.apply(get_wavg)




# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----
# ---- # ---- # ----




# ---- # ---- # ----
# 2.4 Group Transforms and "Unwrapped" GroupBys
# Hay otro metodo diferente a .agg() y .apply() para trabajar con datos agrupados, 
# este es .transform(). 
# La particularidad de este metodo es retorna una Serie  del mismo largo que la Serie 
# como input, a pesar de tomar como referencia los grupos

df = pd.DataFrame({'key': ['a', 'b', 'c'] * 4, 
                   'value': np.arange(12.)}); df

g = df.groupby('key')['value']
g.mean()

#Supongamos que queremos obtener la media de cada grupo, pero queremos un vector con el mismo
#largo que la Serie utilizada para el calculo

g.transform("mean")                 # por medio de una funcion "string"
g.transform(lambda x: x.mean())     # por medio de una funcion lambda

#Como la Serie agrupada esta "Unwrapped" podemos trabajarla como un "array normal". 
def times_two(group): return group * 2
g.transform(times_two)

# En el siguiente ejemplo vemos mas clara la forma de operar de .transform(). 
# A pesar de que nos entrega un array sin agrupar, la operacion .cumsum() opera sobre los grupos
# (Agrego el .join() para poder tener la columna de "key" y ver mas explicita la operacion de la func) 
def times_two(group): return group.cumsum()
g.transform(times_two).join(df["key"]).loc[:,["key","value"]]

#Otro ejemplo usando la funcion .rank()
def get_ranks(group): return group.rank(ascending=False)
g.transform(get_ranks)

#Consideremos el siguiente ejemplo, donde creamos una funcion y la aplicamos por medio de .transform()
#y .apply(). El resultado sera el mismo.

def normalize(x): return (x - x.mean()) / x.std()

g.transform(normalize)
g.apply(normalize)

# Sabemos que las funciones por "string", por ejemplo .agg("mean") o .transform("mean"), estan 
# mejor optimizadas que las que usamos creadas por nosotros. Por ende la misma operacion anterior 
# puede ser hecha de la siguiente forma

normalized = (df['value'] - g.transform('mean')) / g.transform('std'); normalized

#Esta forma en teoria deberia ser mas rapida que la anterior, ese es el beneficio de los 
#"Unwrapped" GroupBys

# ---- # ---- # ----
# 2.5 Group Transforms and "Unwrapped" GroupBys
# "Pivot Tables" son comunmente resumenes de datos encontrados en "spreadsheet program",
# Pandas DataFrame tienen un metodo .pivot_table() y tambien una funcion pd.pivot_table()
# que nos otorgan trabajar los datos como "Pivot Tables". Este metodo/funcion nos permite 
# agregar los totales parciales en los margenes.

#Retomando el DF de tips
tips.head()

#Supongamos que queremos calcular la media para cada columna agrupada por "day" y "smoker".
#Por defecto .pivot_table() trabaja con la media.
tips.pivot_table(index=["day", "smoker"],
                 values=["size", "tip", "tip_pct", "total_bill"])

#Lo anterior lo podriamos haber hecho con un .groupby(["day","smoker"]).mean(). 

#Pero supongamos que queremos agrupar por ["time", "day"], solo dejar las columnas 
#de "tips_pct" y "size", y ademas agrupar por columnas por medio de "smoker"

tips.pivot_table(index=["time", "day"], columns="smoker",
                 values=["tip_pct", "size"])


#Tambien podemos agregar los totales en los margenes
tips.pivot_table(index=["time", "day"], columns="smoker",
                 values=["tip_pct", "size"], margins=True)

#En caso de que queramos utilizar otra funcion que no sea "mean", la agregamos
#por medio del atributo "aggfunc="
tips.pivot_table(index=["time", "smoker"], columns="day",
                 values="tip_pct", aggfunc=len, margins=True)

# En caso de que algun valor de nuestra "pivot table" sea nulo, por medio de 
# "fill_value=" podemos remplazarlo por algun otro valor
tips.pivot_table(index=["time", "size", "smoker"], columns="day",
                 values="tip_pct", fill_value=0)

# ---- # ---- # ----
# 2.6 Cross-Tabulations: Crosstab
# Cross-Tabulations or Crostab en corto, es un caso especial de Pivot Table que nos 
# calcula la frecuencia entre grupos. 

from io import StringIO
data = """Sample  Nationality  Handedness
1   USA  Right-handed
2   Japan    Left-handed
3   USA  Right-handed
4   Japan    Right-handed
5   Japan    Left-handed
6   Japan    Right-handed
7   USA  Right-handed
8   USA  Left-handed
9   Japan    Right-handed
10  USA  Right-handed"""
data = pd.read_table(StringIO(data), sep="\s+")
data

#Podemos contar la cantidad de personas que hay en un pais (USA o JAPAN) en funcion
#de sus tendencia politica
pd.crosstab(data["Nationality"],data["Handedness"], margins=True)

#El primer argumento atiende las filas, el segundo las columnas. Pueden ser una lista
#de Series/Arrays para aumentar el nivel de grupos
pd.crosstab([tips["time"], tips["day"]], tips["smoker"], margins=True)


