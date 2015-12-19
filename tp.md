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
    - 16, {'status': 1, 'office': 1, 'gender': 1, 'age': 50, 'practice': 2, 'law_school': 1, 'seniority': 23}): uno de los socios, hombre de 50 años que estudió en Harvard, trabaja en la oficina de Boston en derecho comercial, y está hace 23 años en la firma.
    - 25, {'status': 1, 'office': 1, 'gender': 1, 'age': 41, 'practice': 1, 'law_school': 3, 'seniority': 15}): uno de los socios, hombre de 41 años que trabaja en la oficina de Boston en el área de litigios, y está hace 15 años en la firma.

  - vértices con mayor grado *out*: abogados (0-indexed) que piden consejos a más personas (grado *out* 27):
    - 15, {'status': 1, 'office': 1, 'gender': 1, 'age': 46, 'practice': 2, 'law_school': 1, 'seniority': 20}: , hombre de 41 años que estudió en Harvard, trabaja en la oficina de Boston en el área de derecho comercial, y está hace 20 años en la firma.

  - vértices con mayor grado total (*in* + *out*): (grado total 50):
    - 16 nuevamente
 
* medidas de centralidad:

 [![betweenness_vertices](https://github.com/diegoo/dmct_tp2/blob/master/betweenness_vertices.png)](#betweenness_vertices)

  - puntos importantes (0-indexed) con medida de betweenness mucho más alta que los demás: 
    - 15, 771.88 {'status': 1, 'office': 1, 'gender': 1, 'age': 46, 'practice': 2, 'law_school': 1, 'seniority': 20}) 
    - 16, 616.86 {'status': 1, 'office': 1, 'gender': 1, 'age': 50, 'practice': 2, 'law_school': 1, 'seniority': 23}) 
    - 59, 432.08 {'status': 2, 'office': 1, 'gender': 2, 'age': 31, 'practice': 2, 'law_school': 2, 'seniority': 2})  
    - 11, 339.08 {'status': 1, 'office': 1, 'gender': 1, 'age': 52, 'practice': 2, 'law_school': 2, 'seniority': 24}) 


### 3. Buscar correlaciones entre medidas de centralidad y atributos de los vértices


### 4.

### 5.

