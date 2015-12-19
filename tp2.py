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
Out[291]: [(16, 29), (25, 29)]




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

red_consejo_centralidad_por_autovalor = red_consejo.evcent()
pylab.plot([vertice.index for vertice in red_consejo.vs], red_consejo_centralidad_por_autovalor)
pylab.xlabel(u"vértice")
pylab.ylabel(u"centralidad")
pylab.title("medida de centralidad: autovalores")
#pylab.show()

# red_consejo_betweenness_normalizados = [x / 771.885 for x in red_consejo_betweenness]
# pylab.plot([vertice.index for vertice in red_consejo.vs], [abs(a - b) for (a,b) in zip(red_consejo_betweenness_normalizados, red_consejo_centralidad_por_autovalor)])

vertice_mayor_betweenness = [x for x in red_consejo.vs if red_consejo_betweenness[x.index] == max(red_consejo_betweenness)][0]
vertice_mayor_closeness = [x for x in red_consejo.vs if red_consejo_closeness[x.index] == max(red_consejo_closeness)][0]
# en ambos casos: 15,{'status': 1, 'office': 1, 'gender': 1, 'age': 46, 'practice': 2, 'law_school': 1, 'seniority': 20})




## 3. buscar correlaciones entre medidas de centralidad y atributos de los vértices

# edad
pylab.hist(red_consejo.vs["age"], bins=35)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["status"]))
(-0.23732194274061164, 0.046285106427618829)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["gender"]))
(-0.051815545105643575, 0.66781823077085289)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["age"]))
(0.16475816855013578, 0.16974028798784357)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["seniority"]))
(0.21122194054899776, 0.07702662066458045)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["office"]))
(-0.14797927383206555, 0.21811473766259087)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["status"]))
(-0.23732194274061164, 0.046285106427618829)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["law_school"]))
(-0.28393163991364734, 0.016413220954138073)

print(pearsonr(red_consejo_betweenness, red_consejo.vs["practice"]))
(0.26813510883890224, 0.02377068212044943)


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
