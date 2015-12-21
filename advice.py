#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *
from lazatt import atributos_de_vertices
import pylab, matplotlib
from itertools import izip
from scipy.stats.stats import pearsonr   
from itertools import groupby
from numpy.random import choice

## 1. construir grafo ADVICE

red_consejo = Graph.Read_Adjacency("lazega.red.consejo.data", mode=ADJ_DIRECTED)
# plot(red_consejo)

red_consejo.vs["status"] =      atributos_de_vertices["status"]  
red_consejo.vs["gender"] =      atributos_de_vertices["gender"]  
red_consejo.vs["office"] =      atributos_de_vertices["office"]  
red_consejo.vs["seniority"] =   atributos_de_vertices["seniority"] 
red_consejo.vs["age"] =         atributos_de_vertices["age"]     
red_consejo.vs["practice"] =    atributos_de_vertices["practice"]
red_consejo.vs["law_school"] =  atributos_de_vertices["law_school"]

# plot(red_consejo)


## 2. caracterización topológica

print(red_consejo.ecount())
print(red_consejo.vcount())
print(red_consejo.diameter())
print(red_consejo.is_directed())
print(red_consejo.is_simple())
print(red_consejo.is_connected())
relaciones_mutuas = [x for x in red_consejo.is_mutual() if x is True]
print(len(relaciones_mutuas) / float(red_consejo.ecount())) # lo mismo: red_consejo.reciprocity()
print(red_consejo.average_path_length())

max_grado_in  = max(red_consejo.degree(mode="in"))
max_grado_out = max(red_consejo.degree(mode="out"))
max_grado_all = max(red_consejo.degree(mode="all"))

nodos_con_maximo_grado_in = filter(lambda v: v.degree(mode="in") == max_grado_in, red_consejo.vs)
nodos_con_maximo_grado_out = filter(lambda v: v.degree(mode="out") == max_grado_out, red_consejo.vs)
nodos_con_maximo_grado_all = filter(lambda v: v.degree(mode="all") == max_grado_all, red_consejo.vs)
print(list(nodos_con_maximo_grado_in))
print(list(nodos_con_maximo_grado_out))
print(list(nodos_con_maximo_grado_all))

# lo mismo:
# nodo_con_maximo_grado_total = red_consejo.vs.select(_degree = red_consejo.maxdegree())
# print(nodo_con_maximo_grado_total.find())

[(a,b) for (a,b) in enumerate(red_consejo.degree(type="in")) if b == red_consejo.maxdegree(type="in")]
# [(16, 29), (25, 29)]

# histograma de grados

xs, ys = zip(*[(left, count) for left, _, count in red_consejo.degree_distribution().bins()])
pylab.xlabel("grado")
pylab.ylabel(u"cantidad de vértices")
pylab.title("grados red ADVICE")
pylab.bar(xs, ys)
# pylab.show()

# medidas de centralidad para vértices
# closeness: distancia relativa a todos los otros vértices
# betweenness: cantidad de caminos más cortos en los que aparece el vértice
# eigenvector centrality:

# plotear x betweenness y evcent:
# low x high y: important gatekeeper to central actor
# high x low y: actor with exclusive access to central actor

red_consejo_betweenness = red_consejo.betweenness()
pylab.plot([vertice.index for vertice in red_consejo.vs], red_consejo_betweenness)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: betweenness")
#pylab.show()

# vértices que se destacan por alto betweenness
[(v,b) for (v,b) in enumerate(red_consejo_betweenness) if b > 300]

red_consejo_closeness = red_consejo.closeness()
pylab.plot([vertice.index for vertice in red_consejo.vs], red_consejo_closeness)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: closeness")
#pylab.show()

# vértices que se destacan por alto closeness (i.e. baja distancia a los otros vértices) 
# [(v,b) for (v,b) in enumerate(red_consejo_closeness) if b < 0.4]

red_consejo_centralidad_por_autovector = red_consejo.evcent()
pylab.plot([vertice.index for vertice in red_consejo.vs], red_consejo_centralidad_por_autovector)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: autovectores")
#pylab.show()

# red_consejo_betweenness_normalizados = [x / 771.885 for x in red_consejo_betweenness]
# pylab.plot([vertice.index for vertice in red_consejo.vs], [abs(a - b) for (a,b) in zip(red_consejo_betweenness_normalizados, red_consejo_centralidad_por_autovector)])

vertice_mayor_betweenness = [x for x in red_consejo.vs if red_consejo_betweenness[x.index] == max(red_consejo_betweenness)]
vertice_mayor_closeness = [x for x in red_consejo.vs if red_consejo_closeness[x.index] == max(red_consejo_closeness)]
vertice_mayor_centralidad_por_autovector = [x for x in red_consejo.vs if red_consejo_centralidad_por_autovector[x.index] == max(red_consejo_centralidad_por_autovector)]

## 3. buscar correlaciones entre medidas de centralidad y atributos de los vértices

# edad
pylab.hist(red_consejo.vs["age"], bins=35)
# pylab.show()

print(pearsonr(red_consejo_betweenness, red_consejo.vs["status"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["gender"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["age"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["seniority"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["office"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["law_school"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["practice"]))

print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["status"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["gender"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["age"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["seniority"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["office"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["law_school"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["practice"]))


## 4. buscar comunidades

# métodos disponibles:

# Graph.community_label_propagation
# Graph.community_edge_betweenness
# Graph.community_walktrap
# Graph.community_infomap
# Graph.community_leading_eigenvector

comunidades_eb = red_consejo.community_edge_betweenness()
clusters_eb = comunidades_eb.as_clustering()
# for cluster, vertices in groupby(clusters_eb lambda x: x[0]): print(cluster, list(vertices))
# cluster_eb_0 = [v for v in red_consejo.vs if v.index in [1, 7, 10, 12, 20, 23, 25, 26, 28, 33, 35, 37, 38, 40, 42, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 69, 70]]
# cluster_eb_1 = [v for v in red_consejo.vs if v.index in [24, 31, 49, 52, 68]]
# el resto, clusters con 1 elemento

comunidades_lp = red_consejo.community_label_propagation()
clusters_lp = sorted([(cluster, vertice) for (vertice, cluster) in zip(range(0, 71), comunidades_lp.membership)])
# for cluster, vertices in groupby(clusters_lp, lambda x: x[0]): print(cluster, len(list(vertices)))

comunidades = red_consejo.community_walktrap()
clusters = comunidades.as_clustering()

print(clusters)
# Clustering with 71 elements and 11 clusters
# [ 0] 0, 1, 3, 6, 7, 9, 11, 13, 14, 15, 16, 18, 19, 21, 22, 27, 29, 32, 34, 36, 43
# [ 1] 2, 4, 5, 17, 24, 31, 45, 49, 50, 52, 68
# [ 2] 8, 10, 12, 20, 23, 25, 26, 28, 33, 37, 39, 42, 44, 46
# [ 3] 30, 35, 47, 48, 57, 67
# [ 4] 38, 40, 41, 51, 53, 55, 56, 58, 60, 65, 66, 69
# [ 5] 54
# [ 6] 59
# [ 7] 61
# [ 8] 62
# [ 9] 63, 70
# [10] 64

cluster0 = [vertice for vertice in red_consejo.vs if vertice.index in clusters[0]]
cluster1 = [vertice for vertice in red_consejo.vs if vertice.index in clusters[1]]
cluster2 = [vertice for vertice in red_consejo.vs if vertice.index in clusters[2]]
cluster3 = [vertice for vertice in red_consejo.vs if vertice.index in clusters[3]]
cluster4 = [vertice for vertice in red_consejo.vs if vertice.index in clusters[4]]

# ver grado de los vértices en los clusters principales
for cluster in [cluster0, cluster1, cluster2, cluster3, cluster4]:
    for vertice in cluster: print vertice, vertice.degree(mode="in"), vertice.degree(mode="out")

# plotear clusters (comunidades)
color_list = [
    'red',    # cluster 0
    'blue',   # cluster 1
    'green',  # cluster 2
    'cyan',   # cluster 3
    'pink',   # cluster 4
    'orange', # ...
    'grey',   
    'yellow', 
    'white',
    'black',
    'purple'
]
# plot(red_consejo, "walktrap_clusters.png", layout="kk", vertex_color=[color_list[x] for x in clusters.membership], vertex_size=5)

# modularidad:
# cuán bien se separan los nodos con diferentes clases o atributos teniendo en cuenta la estructura de la red
# fracción de nodos que caen en los grupos dados, menos la fracción esperada si cayeran al azar
red_consejo_modularidad = red_consejo.modularity(clusters.membership)
print(red_consejo_modularidad)
# 0.15

# modularidad para 1000 agrupamientos al azar
modularidad_random_membership = list()
for i in range(1000):
    modularidad_random_membership.append(red_consejo.modularity(choice(range(0, 11), 71, replace=True).tolist()))

all([red_consejo_modularidad > x for x in modularidad_random_membership])
# True

