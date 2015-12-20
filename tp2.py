#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *
from lazatt import atributos_de_vertices
import pylab, matplotlib
from itertools import izip
from scipy.stats.stats import pearsonr   
from itertools import groupby

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

print(pearsonr(red_consejo_betweenness, red_consejo.vs["status"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["gender"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["age"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["seniority"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["office"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["law_school"]))
print(pearsonr(red_consejo_betweenness, red_consejo.vs["practice"]))

# (-0.23732194274061164, 0.046285106427618829)
# (-0.051815545105643575, 0.66781823077085289)
# (0.16475816855013578, 0.16974028798784357)
# (0.21122194054899776, 0.07702662066458045)
# (-0.14797927383206555, 0.21811473766259087)
# (-0.28393163991364734, 0.016413220954138073)
# (0.26813510883890224, 0.02377068212044943)

print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["status"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["gender"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["age"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["seniority"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["office"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["law_school"]))
print(pearsonr(red_consejo_centralidad_por_autovector, red_consejo.vs["practice"]))

# (-0.68275628890445883, 5.4414842455456928e-11)
# (-0.20988967839008382, 0.078952569368606479)
# (0.52825402910516117, 2.1936856999030843e-06)
# (0.64867071910399554, 9.5307252679818568e-10)
# (-0.20681140897402797, 0.083549177399459204)
# (-0.40234844288785476, 0.00050458116868182961)
# (0.16085302776512134, 0.18022634794134504)


## 4. buscar comunidades

# métodos:

# Graph.community_edge_betweenness
# Graph.community_infomap
# Graph.community_label_propagation
# Graph.community_walktrap
# Graph.community_leading_eigenvector

comunidades = red_consejo.community_edge_betweenness()
clusters = comunidades.as_clustering()
for cluster, vertices in groupby(clusters, lambda x: x[0]): print(cluster, list(vertices))
# (1, [[1, 7, 10, 12, 20, 23, 25, 26, 28, 33, 35, 37, 38, 40, 42, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 69, 70]])
# (24, [[24, 31, 49, 52, 68]])
# el resto, clusters con 1 elemento
cluster1 = [v for v in red_consejo.vs if v.index in [1, 7, 10, 12, 20, 23, 25, 26, 28, 33, 35, 37, 38, 40, 42, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 69, 70]]
cluster24 = [v for v in red_consejo.vs if v.index in [24, 31, 49, 52, 68]]

comunidades = red_consejo.community_label_propagation()
clusters_con_vertices = sorted([(cluster, vertice) for (vertice, cluster) in zip(range(0, 71), comunidades.membership)])
for cluster, vertices in groupby(clusters_con_vertices, lambda x: x[0]): print(cluster, len(list(vertices)))
cluster0 = [v for v in red_consejo.vs if v.index in [b for (a,b) in [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29), (0, 30), (0, 31), (0, 32), (0, 33), (0, 34), (0, 35), (0, 36), (0, 37), (0, 38), (0, 39), (0, 40), (0, 41), (0, 42), (0, 44), (0, 45), (0, 47), (0, 48), (0, 49), (0, 50), (0, 51), (0, 52), (0, 53), (0, 54), (0, 55), (0, 56), (0, 57), (0, 59), (0, 63), (0, 64), (0, 69)]]]
# (0, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29), (0, 30), (0, 31), (0, 32), (0, 33), (0, 34), (0, 35), (0, 36), (0, 37), (0, 38), (0, 39), (0, 40), (0, 41), (0, 42), (0, 44), (0, 45), (0, 47), (0, 48), (0, 49), (0, 50), (0, 51), (0, 52), (0, 53), (0, 54), (0, 55), (0, 56), (0, 57), (0, 59), (0, 63), (0, 64), (0, 69)])
# (3, [(3, 58), (3, 68)])
# (4, [(4, 60), (4, 61)])
# (1, [(1, 43)])
# (2, [(2, 46)])
# (5, [(5, 62)])
# (6, [(6, 65)])
# (7, [(7, 66)])
# (8, [(8, 67)])
# (9, [(9, 70)])

comunidades = red_consejo.community_walktrap()
clusters = comunidades.as_clustering()
for cluster, vertices in groupby(clusters, lambda x: x[0]): print(cluster, list(vertices))
cluster0 = [v for v in red_consejo.vs if v.index in [0, 1, 3, 6, 7, 9, 11, 13, 14, 15, 16, 18, 19, 21, 22, 27, 29, 32, 34, 36, 43]]
cluster2 = [v for v in red_consejo.vs if v.index in [2, 4, 5, 17, 24, 31, 45, 49, 50, 52, 68]]
cluster8 = [v for v in red_consejo.vs if v.index in [8, 10, 12, 20, 23, 25, 26, 28, 33, 37, 39, 42, 44, 46]]
cluster30 = [v for v in red_consejo.vs if v.index in [30, 35, 47, 48, 57, 67]]
cluster38 = [v for v in red_consejo.vs if v.index in [38, 40, 41, 51, 53, 55, 56, 58, 60, 65, 66, 69]]
# (0, [[0, 1, 3, 6, 7, 9, 11, 13, 14, 15, 16, 18, 19, 21, 22, 27, 29, 32, 34, 36, 43]])
# (2, [[2, 4, 5, 17, 24, 31, 45, 49, 50, 52, 68]])
# (8, [[8, 10, 12, 20, 23, 25, 26, 28, 33, 37, 39, 42, 44, 46]])
# (30, [[30, 35, 47, 48, 57, 67]])
# (38, [[38, 40, 41, 51, 53, 55, 56, 58, 60, 65, 66, 69]])
# (63, [[63, 70]])
# (54, [[54]])
# (59, [[59]])
# (61, [[61]])
# (62, [[62]])
# (64, [[64]])






comunidades_por_infomap = Graph.community_infomap(red_consejo)

for comunidades in [comunidades_por_infomap, comunidades_por_edge_betweenness]:
    summary(comunidades)
    n = comunidades.optimal_count
    communities.as_clustering(num_communities)

red_consejo_clusters = red_consejo.community_edge_betweenness().as_clustering()
membresias = red_consejo_clusters.membership
for observacion, membresia in izip(red_consejo, membresias):
    print(observacion, membresias)
