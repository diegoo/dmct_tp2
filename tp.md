## Tareas específicas

### 1. Construir redes

1era red: Los primeros 71 registros de la tabla original. Es la red "ADVICE".
La relación modelada por cada arista es "X buscó a Y para pedirle consejo profesional".

### 2. Caracterizar topología de las redes

1era red

* tipo de red:			  grafo dirigido
* ¿conectado?:			  no
* ¿simple?:			  sí
* número de vértices: 		  71
* número de aristas: 		  612 
* densidad: 			  0.12313883299798792
* diámetro:			  5
* porcentaje de aristas simétricas: 17 %
* longitud de camino promedio:	  2.33
* análisis de grados:

  - plot histograma de grados

 [![histograma_grados](https://github.com/diegoo/dmct_tp2/blob/master/histograma_grados_red_consejos.png)](#grados)

  - vértices con mayor grado *in*: abogados (0-indexed) a quienes más les piden consejos (grado *in* 29):
    - 17 (16), {'status': 1, 'office': 1, 'gender': 1, 'age': 50, 'practice': 2, 'law_school': 1, 'seniority': 23}): uno de los socios, hombre de 50 años que estudió en Harvard, trabaja en la oficina de Boston en derecho comercial, y está hace 23 años en la firma.
    - 26 (25), {'status': 1, 'office': 1, 'gender': 1, 'age': 41, 'practice': 1, 'law_school': 3, 'seniority': 15}): uno de los socios, hombre de 41 años que trabaja en la oficina de Boston en el área de litigios, y está hace 15 años en la firma.

  - vértices con mayor grado *out*: abogados (0-indexed) que piden consejos a más personas (grado *out* 27):
    - 16 (15), {'status': 1, 'office': 1, 'gender': 1, 'age': 46, 'practice': 2, 'law_school': 1, 'seniority': 20}: , hombre de 41 años que estudió en Harvard, trabaja en la oficina de Boston en el área de derecho comercial, y está hace 20 años en la firma.

  - vértices con mayor grado total (*in* + *out*): (grado total 50):
    - 17 (16) nuevamente
 
* medidas de centralidad:

 [![betweenness_vertices](https://github.com/diegoo/dmct_tp2/blob/master/betweenness_vertices.png)](#betweenness_vertices)

  - puntos importantes (0-indexed) con medida de betweenness mucho más alta que los demás: 
    - 16 (15), 771.88 {'status': 1, 'office': 1, 'gender': 1, 'age': 46, 'practice': 2, 'law_school': 1, 'seniority': 20}) 
    - 17 (16), 616.86 {'status': 1, 'office': 1, 'gender': 1, 'age': 50, 'practice': 2, 'law_school': 1, 'seniority': 23}) 
    - 60 (59), 432.08 {'status': 2, 'office': 1, 'gender': 2, 'age': 31, 'practice': 2, 'law_school': 2, 'seniority': 2})  
    - 12 (11), 339.08 {'status': 1, 'office': 1, 'gender': 1, 'age': 52, 'practice': 2, 'law_school': 2, 'seniority': 24}) 

  Llama la atención el vértice 59, porque se diferencia del resto: es mujer, es joven, no es socia, y estuvo pocos años en la empresa.

 [![autovectores_vertices](https://github.com/diegoo/dmct_tp2/blob/master/autovectores_vertices.png)](#autovectores_vertices)
 
  - puntos importantes (0-indexed) con alta medida de centralidad por autovector:
    - 17 (16), 1.00 {'status': 1, 'office': 1, 'gender': 1, 'age': 50, 'practice': 2, 'law_school': 1, 'seniority': 23}) 
    - 26 (25), 0.74 {'status': 1, 'office': 1, 'gender': 1, 'age': 41, 'practice': 1, 'law_school': 3, 'seniority': 15})


### 3. Buscar correlaciones entre medidas de centralidad y atributos de los vértices

Si calculamos la correlación de Pearson entre los vectores de centralidad por autovector y los vectores de cada uno de los atributos, las correlaciones con p-valor más significativos son:
   - status (0.68)
   - seniority (0.64)
   - age (0.52)

 [![edad](https://github.com/diegoo/dmct_tp2/blob/master/edad.png)](#edad)
 
Los 3 atributos están relacionados. Edad y seniority van de la mano, y el status de partner se alcanza después de años como associate. El histograma de la distribución de edades muestra que la firma sigue la tradición *up-or-out*: los abogados que no mejoran su desempeño para seguir ascendiendo después de cierta edad, se van. Por eso hay picos entre los de 30 que hacen el trabajo duro y los de 45-60 que llegaron a partners, pero hay un hueco alrededor de los 40.


### 4. Buscar comunidades y determinar si hay asociación entre comunidades y características personales

El método de *label propagation* genera 11 clusters (uno muy grande, y 10 de tamaño 1), sin agrupación discernible.

El método de *edge_betweenness* (la idea de que hay aristas con alta centralidad que conectan comunidades y se pueden quitar iterativamene para generar un dendrograma) genera 36 clusters (uno de tamaño 32, uno de 5, el resto de 1); el cluster mayoritario tiene abogados de la oficina de Boston (29/32); 11 socios, 21 no-socios.

El método más efectivo para encontrar comunidades resultó ser *walktrap* (la idea de que random walks breves tienden a quedarse en la misma comunidad). Con este método se obtuvieron 11 clusters (de tamaños 21,14,12,11,6,2,1,1,1,1,1). El cluster más grande (cluster 0) parece agrupar a socios de la firma (19/21), otro cluster (cluster 1) agrupa abogados de la oficina de Hartford (9/11), otro (cluster 2) agrupa el resto de los socios de la oficina principal, y otro (cluster 4) agrupa a empleados no-socios de la oficina de Boston (11/12).

Un análisis del grado de los individuos en la red de consejos revela estos datos sobre sus comunidades:

 [![walktrap_clusters](https://github.com/diegoo/dmct_tp2/blob/master/walktrap_clusters.png)](#walktrap_clusters)

 - cluster 0 (en rojo): Los socios importantes, dan y reciben consejo entre pares. Son los más buscados y, en su mayoría, muy dispuestos a consultar a otros => los más centrales en la red.
  
 - cluster 1 (en azul): Grupo que resulta de la polarización entre oficinas.
  
 - cluster 2 (en verde): El escalón de socios que sigue en importancia al cluster 0. Son muy buscados por su autoridad, pero menos dispuestos a pedir consejo que los miembros del cluster 0.
  
 - cluster 4 (en rosa): Son *associates* (empleados no-socios), con poco seniority. Piden consejo a otros, pero ellos mismos son poco buscados por su consejo (grado saliente > grado entrante). En el libro de Lazega se corresponden con el cluster periférico llamado "the boys" (en criollo, los "che pibe" que hacen el trabajo de base, es decir, no los que toman las decisiones).

Para evaluar el agrupamiento en comunidades, calculamos su modularidad: 0.15. Como se cumple que este valor es siempre mayor que el valor de modularidad calculado para 1000 agrupamientos al azar, concluimos que es significativo (cf. código en apéndice *advice.py*)


### 5.

Del análisis de la red de consejos se desprenden algunas conclusiones:

- La red existe porque la firma trató de evitar la burocracia de los mecanismos formales de *peer review*. Si hubiera un mecanismo formal, la red sería mucho más jerárquica y vertical.

- Es una red armada alrededor de la distribución de conocimientos, y ese conocimiento se gana con la experiencia (por eso los partners más senior son centrales, incluso cuando hay jóvenes que los superan en educación; el consejo en general no tiene que ver con la Ley, sino con el trato de clientes, y eso se gana con los años en la empresa).

- Fuera del núcleo central, en el resto de los clusters los abogados buscan consejo en su entorno, y fuera de su entorno sólo cuando es necesario. El sistema de consejo se establece por tarea, pero está predominantemente guiado por seniority. La red de consejo es bastante jerárquica (no se busca consejo "hacia abajo"). 

- En un momento hubo una fusión entre empresas y por eso ahora hay varias oficinas. La oficina 1 era la central, pero la oficina 2 tenía clientes más grandes (p. 76); esas diferencias hicieron surgir cierta rivalidad entre las oficinas. Esa tendencia al aislamiento fue detectada, y la podemos confirmar con el cluster de la oficina 2. La fusión también trajo conflictos de "cultura" o forma de hacer las cosas. No todas las especialidades estaban representadas en todas las oficinas, entonces un partner a veces tenía que consultar a un associate de otra oficina, pero en general los abogados tenían una opinión superficial sobre los de otras oficinas. El aislamiento en la firma se quiso contrarrestar con mecanismos sociales "informales".

- En vista de todo esto, una posible sugerencia sería implementar algún sistema de rotación, donde los associates tengan que cambiar de oficina a cambio de un ascenso y compensación monetaria. Boston y Providence quedan cerca: Hartford queda a unas 2 horas en auto. Con esa medida se forjarían más lazos entre los equipos.


