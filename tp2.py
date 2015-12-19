#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *
from lazatt import atributos_de_vertices
import pylab, matplotlib
from itertools import izip
from scipy.stats.stats import pearsonr   


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

red_consejo_centralidad_por_autovalor = red_consejo.evcent()
pylab.plot([vertice.index for vertice in red_consejo.vs], red_consejo_centralidad_por_autovalor)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: autovalores")
#pylab.show()

# red_consejo_betweenness_normalizados = [x / 771.885 for x in red_consejo_betweenness]
# pylab.plot([vertice.index for vertice in red_consejo.vs], [abs(a - b) for (a,b) in zip(red_consejo_betweenness_normalizados, red_consejo_centralidad_por_autovalor)])

vertice_mayor_betweenness = [x for x in red_consejo.vs if red_consejo_betweenness[x.index] == max(red_consejo_betweenness)]
vertice_mayor_closeness = [x for x in red_consejo.vs if red_consejo_closeness[x.index] == max(red_consejo_closeness)]
vertice_mayor_centralidad_por_autovalor = [x for x in red_consejo.vs if red_consejo_centralidad_por_autovalor[x.index] == max(red_consejo_centralidad_por_autovalor)]

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

print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["status"]))
print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["gender"]))
print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["age"]))
print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["seniority"]))
print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["office"]))
print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["law_school"]))
print(pearsonr(red_consejo_centralidad_por_autovalor, red_consejo.vs["practice"]))

# (-0.68275628890445883, 5.4414842455456928e-11)
# (-0.20988967839008382, 0.078952569368606479)
# (0.52825402910516117, 2.1936856999030843e-06)
# (0.64867071910399554, 9.5307252679818568e-10)
# (-0.20681140897402797, 0.083549177399459204)
# (-0.40234844288785476, 0.00050458116868182961)
# (0.16085302776512134, 0.18022634794134504)


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
