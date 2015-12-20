library(readxl)
library(foreign)
library(igraph)
library(ggplot2)

# crear red FRIENDSHIP y asignarle atributos a los vértices
lazega <- read.table("lazega.dat", skip = 8)
lazega_attributes <- read.table("lazatt.dat", skip = 12)
colnames(lazega_attributes) = c("Obs", "STATUS", "GENDER", "OFFICE", "SENIORITY", "AGE", "PRACTICE", "LAW_SCHOOL")
lazega_attributes = list(Obs = lazega_attributes$Obs, STATUS = lazega_attributes$STATUS, GENDER = lazega_attributes$GENDER, OFFICE = lazega_attributes$OFFICE, SENIORITY = lazega_attributes$SENIORITY, AGE = lazega_attributes$AGE, PRACTICE = lazega_attributes$PRACTICE, LAW_SCHOOL = lazega_attributes$LAW_SCHOOL)
lazega.matrix <- as.matrix(lazega)
amistad.matrix <- as.matrix(lazega[72:142,])
amistad <- graph.adjacency(amistad.matrix, mode="undirected", diag = FALSE, weighted = T)
vertex_attr(amistad) <- lazega_attributes
plot(amistad.red)
