#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *
from lazatt import atributos_de_vertices
import pylab, matplotlib
from itertools import izip


## 1.1 construir grafo ADVICE

red_consejo = Graph.Read_Adjacency("lazega.red.consejo.data", mode=ADJ_DIRECTED))
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
nodo_con_maximo_grado = red_consejo.vs.select(_degree = red_consejo.maxdegree())
print(nodo_con_maximo_grado.find())

# histograma de grados

xs, ys = zip(*[(left, count) for left, _, count in red_consejo.degree_distribution().bins()])
pylab.xlabel("grado")
pylab.ylabel(u"cantidad de vértices")
pylab.title("grados red ADVICE")
pylab.bar(xs, ys)
# pylab.show()


## 3. buscar correlaciones entre medidas de centralidad y atributos de los vértices


## 4. buscar comunidades

# armar comunidades con varios métodos

funciones_deteccion_comunidad = [
    Graph.community_edge_betweenness,
    Graph.community_infomap,
    Graph.community_label_propagation,
    Graph.community_walktrap,
    Graph.community_leading_eigenvector
]

red_consejo_comunidades_por_metodo = [f(red_consejo) for f in funciones_deteccion_comunidad]

for comunidades in red_consejo_comunidades_por_metodo:
    print summary(comunidad)
    n = communities.optimal_count
    communities.as_clustering(num_communities)

red_consejo_clusters = red_consejo.community_edge_betweenness().as_clustering()
membresias = red_consejo_clusters.membership
for observacion, membresia in izip(red_consejo, membresias):
    print(observacion, membresias)
