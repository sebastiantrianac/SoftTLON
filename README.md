# TLON

TLÖN es un sistema de cómputo propuesto por el grupo de investigación en redes de Telecomunicaciones Dinámicas y lenguajes de programación distribuidos de la Universidad Nacional de Colombia. El modelo que propone TLÖN es un esquema social inspirado que plantea una analogía entre los conceptos de Justicia de Rawls, Inmanencia de Spinoza, Estado de Hobbes, Paradigma de Kuhn y existencia y esencia de Sartre, abstraídos al plano de virtualización de una red inalámbrica. Cada capa del sistema TLÖN (Figura 4) representa un nivel en la analogía del Estado; inicialmente una capa física del modelo (Territorio) que será una red AdHoc inalámbrica que planteará las condiciones de prestación de los servicios de las capas superiores. La capa de virtualización se puede entender como la función de control que deben ejercer las instituciones de un estado. El concepto de sociedad vendría implícito en la capa del sistema Multiagente, como un conjunto de individuos que interactúan entre sí y con las otras capas del sistema con el fin de prestar y consumir servicios.

Figura 4. Capas del sistema de cómputo TLÖN
![alt text](https://raw.githubusercontent.com/sebastiantrianac/SoftTLON/images/TLON.jpeg)

## SoftTLON

### Distributed Processing - distProc:

Library for distributed processing

----
```PYTHON
import MultiPManager.distProc
```
----

### tlon_parallelize

Create the desired {resource} in its JSON representation. The resource shall be part of the designer models known in the final project, as the JSON representation is explicitly parsed relying on the {resource} reference.

----
```PYTHON
tlon_parallelize(<function>, <data_set>)
```
----
