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



