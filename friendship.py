#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *
from lazatt import atributos_de_vertices
import pylab, matplotlib
from itertools import izip
from scipy.stats.stats import pearsonr   
from itertools import groupby

## 1. construir grafo FRIENDSHIP

red_amistad = Graph.Read_Adjacency("lazega.red.amistad.data", sep=',', mode=ADJ_UNDIRECTED)

red_amistad.vs["status"] =      atributos_de_vertices["status"]  
red_amistad.vs["gender"] =      atributos_de_vertices["gender"]  
red_amistad.vs["office"] =      atributos_de_vertices["office"]  
red_amistad.vs["seniority"] =   atributos_de_vertices["seniority"] 
red_amistad.vs["age"] =         atributos_de_vertices["age"]     
red_amistad.vs["practice"] =    atributos_de_vertices["practice"]
red_amistad.vs["law_school"] =  atributos_de_vertices["law_school"]

# plot(red_amistad)


## 2. caracterización topológica

print(red_amistad.ecount())
print(red_amistad.vcount())
print(red_amistad.diameter())
print(red_amistad.is_directed())
print(red_amistad.is_simple())
print(red_amistad.is_connected())
print(red_amistad.average_path_length())

max_grado  = max(red_amistad.degree())
nodos_con_maximo_grado = filter(lambda v: v.degree() == max_grado, red_amistad.vs)
print(list(nodos_con_maximo_grado))

# histograma de grados

xs, ys = zip(*[(left, count) for left, _, count in red_amistad.degree_distribution().bins()])
pylab.xlabel("grado")
pylab.ylabel(u"cantidad de vértices")
pylab.title("grados red FRIENDSHIP")
pylab.bar(xs, ys)
# pylab.show()

# medidas de centralidad para vértices
# closeness: distancia relativa a todos los otros vértices
# betweenness: cantidad de caminos más cortos en los que aparece el vértice
# eigenvector centrality:

# plotear x betweenness y evcent:
# low x high y: important gatekeeper to central actor
# high x low y: actor with exclusive access to central actor

red_amistad_betweenness = red_amistad.betweenness()
pylab.plot([vertice.index for vertice in red_amistad.vs], red_amistad_betweenness)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: betweenness")
#pylab.show()

# vértices que se destacan por alto betweenness
# [(v,b) for (v,b) in enumerate(red_amistad_betweenness) if b > 300]

red_amistad_closeness = red_amistad.closeness()
pylab.plot([vertice.index for vertice in red_amistad.vs], red_amistad_closeness)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: closeness")
#pylab.show()

# vértices que se destacan por alto closeness (i.e. baja distancia a los otros vértices) 
# [(v,b) for (v,b) in enumerate(red_amistad_closeness) if b < 0.4]

red_amistad_centralidad_por_autovector = red_amistad.evcent()
pylab.plot([vertice.index for vertice in red_amistad.vs], red_amistad_centralidad_por_autovector)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: autovectores")
#pylab.show()

vertice_mayor_betweenness = [x for x in red_amistad.vs if red_amistad_betweenness[x.index] == max(red_amistad_betweenness)]
vertice_mayor_closeness = [x for x in red_amistad.vs if red_amistad_closeness[x.index] == max(red_amistad_closeness)]
vertice_mayor_centralidad_por_autovector = [x for x in red_amistad.vs if red_amistad_centralidad_por_autovector[x.index] == max(red_amistad_centralidad_por_autovector)]

## 3. buscar correlaciones entre medidas de centralidad y atributos de los vértices

# edad
pylab.hist(red_amistad.vs["age"], bins=35)
# pylab.show()

print(pearsonr(red_amistad_betweenness, red_amistad.vs["status"]))
print(pearsonr(red_amistad_betweenness, red_amistad.vs["gender"]))
print(pearsonr(red_amistad_betweenness, red_amistad.vs["age"]))
print(pearsonr(red_amistad_betweenness, red_amistad.vs["seniority"]))
print(pearsonr(red_amistad_betweenness, red_amistad.vs["office"]))
print(pearsonr(red_amistad_betweenness, red_amistad.vs["law_school"]))
print(pearsonr(red_amistad_betweenness, red_amistad.vs["practice"]))

print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["status"]))
print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["gender"]))
print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["age"]))
print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["seniority"]))
print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["office"]))
print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["law_school"]))
print(pearsonr(red_amistad_centralidad_por_autovector, red_amistad.vs["practice"]))


## 4. buscar comunidades

# métodos disponibles:

# Graph.community_label_propagation
# Graph.community_edge_betweenness
# Graph.community_walktrap
# Graph.community_infomap
# Graph.community_leading_eigenvector

comunidades_eb = red_amistad.community_edge_betweenness()
clusters_eb = comunidades_eb.as_clustering()
# 1 cluster, y 45 clusters unitarios

comunidades_lp = red_amistad.community_label_propagation()
clusters_lp = sorted([(cluster, vertice) for (vertice, cluster) in zip(range(0, 71), comunidades_lp.membership)])
# 1 cluster (?)

comunidades = red_amistad.community_walktrap()
clusters = comunidades.as_clustering()

print(clusters)
# Clustering with 71 elements and 3 clusters
# [0] 0, 2, 7, 10, 12, 20, 22, 23, 26, 35, 37, 38, 39, 40, 42, 48, 51, 53, 54,
#     55, 56, 64, 65, 66, 67, 68, 70
# [1] 1, 3, 6, 8, 9, 11, 14, 15, 16, 18, 19, 21, 25, 28, 33, 36, 41, 43, 44, 45,
#     46, 47, 52, 59, 60, 61, 63, 69
# [2] 4, 5, 13, 17, 24, 27, 29, 30, 31, 32, 34, 49, 50, 57, 58, 62

cluster0 = [vertice for vertice in red_amistad.vs if vertice.index in clusters[0]]
cluster1 = [vertice for vertice in red_amistad.vs if vertice.index in clusters[1]]
cluster2 = [vertice for vertice in red_amistad.vs if vertice.index in clusters[2]]

# ver grado de los vértices en los clusters principales
for cluster in [cluster0, cluster1, cluster2]:
    print(cluster)
    for vertice in cluster: 
        print vertice, vertice.degree()

# plotear clusters (comunidades)
color_list = [
    'red',    # cluster 0
    'blue',   # cluster 1
    'green',  # cluster 2
    'orange'
]
plot(red_amistad, "walktrap_clusters_amistad.png", layout="kk", vertex_color=[color_list[x] for x in clusters.membership], vertex_size=5)
