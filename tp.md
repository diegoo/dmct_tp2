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

  - vértice con mayor grado: observación nro. 17 (16 si 0-indexed), con grado 50.
    {'status': 1,
     'office': 1,
     'gender': 1,
     'age': 50,
     'practice': 2,
     'law_school': 1,
     'seniority': 23}) => el más consultado es uno de los socios,
     		       	  hombre de 50 años que estudió en Harvard,
			  trabaja en la oficina de Boston en derecho
			  comercial, y está hace 23 años en la firma.

medidas de centralidad:


### 3. Buscar correlaciones entre medidas de centralidad y atributos de los vértices

### 4.

### 5.

