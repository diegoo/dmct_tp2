#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *
from lazatt import atributos_de_vertices

red_coworkers = Graph.Read_Adjacency("lazega.red.coworkers.data")

red_coworkers.vs["status"] =      atributos_de_vertices["status"]  
red_coworkers.vs["gender"] =      atributos_de_vertices["gender"]  
red_coworkers.vs["office"] =      atributos_de_vertices["office"]  
red_coworkers.vs["seniority"] =   atributos_de_vertices["seniority"] 
red_coworkers.vs["age"] =         atributos_de_vertices["age"]     
red_coworkers.vs["practice"] =    atributos_de_vertices["practice"]
red_coworkers.vs["law_school"] =  atributos_de_vertices["law_school"]

# plot(red_coworkers)

funciones_deteccion_comunidad = [
    Graph.community_edge_betweenness,
    Graph.community_infomap,
    Graph.community_label_propagation,
    Graph.community_walktrap,
    Graph.community_leading_eigenvector
]

red_coworkers_comunidades = [f(red_coworkers) for f in funciones_deteccion_comunidad]

for comunidad in red_coworkers_comunidades: print summary(comunidad)







    
num_communities = communities.optimal_count
communities.as_clustering(num_communities)

# calculate dendrogram
dendrogram = graph.community_edge_betweenness()

# convert it into a flat clustering
clusters = dendrogram.as_clustering()

# get the membership vector
membership = clusters.membership

# Now we can start writing the membership vector along with the node names into a CSV file::

import csv
from itertools import izip

writer = csv.writer(open("output.csv", "wb"))
for name, membership in izip(graph.vs["name"], membership):
    writer.writerow([name, membership])
