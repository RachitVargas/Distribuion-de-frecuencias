"""Distribución de frecuencia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cy8jehDKvMx9XrBLa06BYhAGKDyWnMoM

# Distribución de frecuencias - Estadistíca y probabilidad
## Rachit Vargas

---

<img src=https://biblioteca.ulead.ac.cr/sites/default/files/LEAD%20color.png  width="200"></img></a>
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import math

df = pd.read_csv('/content/data.csv', sep=';', decimal=',')

class Distribucion_frecuencia():
  
  def __init__(self, datos, col):
    self.__datos = datos
    self.__col = col
    self.__tabla_frecuencia = self.__tabla(self.__datos, self.__col)

  @property
  def datos(self):
    return self.__datos

  @datos.setter
  def datos(self, datos):
    self.__datos = datos

  @property
  def col(self):
    return self.__col

  @datos.setter
  def col(self, col):
    self.__col = col

  @property
  def tabla_frecuencia(self):
    return self.__tabla_frecuencia
  
  def analisis(self):
    print('*** [CABECERA] ***: \n ' + str(self.__datos.head()))
    print('*** [ESTADISTICA BASICA] ***: \n' + str(self.__datos.describe()))
    print('*** [DIMENSION] *** filas:' + 
          str(self.__datos.shape[0]) + ' ; columnas:' + str(self.__datos.shape[1]))
    print(self.__tabla_frecuencia.dtypes)
    print(self.__datos.boxplot())

  def plot_hist(self, x, y, titulo='Histograma de frecuencia', 
                xlabel='Vida util en años', ylabel='Frecuencia Absoluta acomulada'):
    
    sns.barplot(x=x, y=y, data=self.__tabla_frecuencia)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

  def plot_line(self, x, y, titulo='Histograma de frecuencia', 
                xlabel='Vida util en años', ylabel='Frecuencia Absoluta acomulada', 
                ind_labels=True):

    x = self.__tabla_frecuencia[x]
    y = self.__tabla_frecuencia[y]
    sns.scatterplot(x=x,y=y)
    sns.lineplot(x=x,y=y)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ind_labels:
          for i, txt in enumerate(self.__tabla_frecuencia.nk):
              plt.annotate(txt, (x[i], y[i]))

  def __agrupar(self, li, ls, intervalos, c, name='intervalos', closed='right'):
    grupos = pd.interval_range(start=li,  periods=intervalos, freq=c,
                               name=name, closed=closed)
    return grupos

  def __crear_tabla(self, grupos, datos, col, intervalos):
    tabla = pd.DataFrame(index=grupos)
    tabla['nk'] = pd.cut(datos[col], bins=tabla.index).value_counts()
    tabla['li'] = tabla.index.left
    tabla['ls'] = tabla.index.right
    tabla['pm'] = np.round((tabla['li']+tabla['ls'])/2,2)
    tabla['fk'] = tabla['nk']/len(datos)

    nk_acum = []  
    valor = 0
    for i in range(intervalos):
      if len(nk_acum)==0:
        valor = valor + tabla.iloc[i,0]
        nk_acum.append(valor)
      else:
        valor = valor + tabla.iloc[i,0]
        nk_acum.append(valor)
  
    tabla['nk_acum'] = nk_acum

    fk_acum = (tabla['nk_acum']/sum(tabla['nk']))
    tabla['fk_acum'] = fk_acum
    return tabla

  def __tabla(self, datos, col):
    k = 1 + 3.3 * math.log10(len(datos))
    intervalos = math.ceil(k)

    li = min(datos[col])-0.1/2
    ls = max(datos[col])+0.1/2
    
    rango = ls-li

    c = np.round(rango/intervalos, 2)
    grupos = self.__agrupar(li, ls, intervalos, c)
    tabla = self.__crear_tabla(grupos, datos, col, intervalos)
    tabla = tabla.reset_index()
    return tabla

distribucion = Distribucion_frecuencia(datos=df, col='VidaUtil')

distribucion.analisis()

"""## Abreviaturas:

Frecuencia absoluta $ = nk \longrightarrow \sum_{i=1}^{k} n_i = n_1 + n_2 ... n_k$ \\

Limite inferior $ = li \longrightarrow [n_i -- )$ \\

Limite superior $ = ls \longrightarrow [ -- n_i)$ \\

Punto medio $ = pm \longrightarrow pm = \frac{(li + ls)}{2}$ \\

Frecuencia relativa $ = fk \longrightarrow f_k = \frac{n_k}{N}$ \\

Frecuencia absoluta acumulada $ = nk\_acum \longrightarrow N_i = n_1 + n_2 + ... + n_i$ \\

Frecuencia relativa acumulada $ = fk\_acum \longrightarrow F_i = \frac{N_i}{N}$ \\
"""

distribucion.tabla_frecuencia

plt.figure(figsize=(10,7))
distribucion.plot_hist(x='pm', y='nk')

plt.figure(figsize=(10,7))
distribucion.plot_line(x='pm', y='nk')

plt.figure(figsize=(10,7))
distribucion.plot_hist(x='pm', y='nk_acum')

plt.figure(figsize=(10,7))
distribucion.plot_line(x='pm', y='nk_acum')
