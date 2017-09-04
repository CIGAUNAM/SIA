# encoding: utf-8
#

# ===================================================================
# Módulo vectSim.py
# ===================================================================
# Funciones para calcular la similitud entre vectores.
#
# Se requiere la biblioteca NUMPY
#
#


import numpy as np

# Norma de un vector
# ===================================================================
# INPUT:
#       v - Arreglo de numpy
# OUTPUT:
#       n - Norma euclidiana del vector v (float)
def norm(v):
    return np.sqrt(np.dot(v, v))


# Distancia euclidiana entre vectores
# ===================================================================
# INPUT:
#       A,B - Vectores cuya distancia se desea calcular. Pueden ser
#             listas o arreglos de numpy
# OUTPUT:
#       d   - Distancia entre los vectores A y B usando la norma
#             norma euclidiana
def eucl(A,B):
    a = np.array(A, float)
    b = np.array(B, float)
    return norm(a - b)


# Coseno
# ===================================================================
# INPUT:
#       a,b - Vectores cuya distancia se desea calcular. Pueden ser
#             listas o arreglos de numpy
# OUTPUT:
#       d   - Coseno del ángulo entre vectores (float)
def cosDist(A, B):
    a = np.array(A, float)
    b = np.array(B, float)
    denominador = norm(a)*norm(b)
    return np.dot(a,b)/denominador if denominador != 0 else 0


# Promedio de los elementos de un vector
# ===================================================================
# INPUT:
#       A - Vector en forma de lista o arreglo de numpy
# OUTPUT:
#       p - Promedio de los elementos en A
def prom(A):
    a = np.array(A, float)
    return np.sum(a) / np.sum(a != 0)



# Coseno ajustado del ángulo entre vectores
# ===================================================================
# INPUT:
#       A,B - Vectores cuya similitud desea calcularse. Pueden ser
#             listas o arreglos de numpy
# OUTPUT:
#       d   - Coseno AJUSTADO del ángulo entre vectores. En esta
#             esta medida se considera el ángulo que forman los
#             vectores previamente centrados. Esta medida se
#             describe en la Sección 3 del documento.

def adjustedCosine(A,B):
    a = np.array(A, float)
    b = np.array(B, float)

    #centered vectors
    a[a!=0] -= prom(a)
    b[b!=0] -= prom(b)
    return cosDist(a, b)


# Rutina que compara un vector contra una tabla de datos dada
# ===================================================================
# INPUT:
#       A - Arreglo de numpy, m x n, que representa los datos
#           conocidos en el sistema de recomendacion. Cada columna
#           representa un elemento del conjunto a considerar,
#           usuario (filtrado colaborativo) u objeto (recomendación
#           basada en contenido).
#
#       v - Arreglo de numpy con m elementos.
#           Representa un vector relacionado con un nuevo usuario
#           (u objeto) que desea compararse con las columnas de A.
#
#       simFunction - (Argumento opcional)
#           Función que se usará para determinar la similitud entre
#           vectores. Si este argumento no se especifica, se usa
#           la distancia euclidiana entre vectores
#           (función eucl de este módulo).
# OUTPUT:
#       I - Lista que contiene los índices de las columnas de A
#           en orden de mayor a menor similitud respecto al
#           vector v (orden ascendente, en el caso de la
#           distancia euclidiana).

def comparar_TablaVector(A, v, N, simFunction=eucl):
    m, n = A.shape
    temp = []

    for i in range(n):
        dist = simFunction(A[:, i].flatten(), v)
        temp.append((i, dist))

    booleano = (True if simFunction!=eucl else False)
    temp.sort(key=lambda x: x[1],reverse=booleano)
    I = [temp[t][0] for t in range(N)]
    similitudes = [temp[t][1] for t in range(N)]
    return I,np.array(similitudes)
