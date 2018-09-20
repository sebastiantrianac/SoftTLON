# TLON

TLÖN es un sistema de cómputo propuesto por el grupo de investigación en redes de Telecomunicaciones Dinámicas y lenguajes de programación distribuidos de la Universidad Nacional de Colombia. El modelo que propone TLÖN es un esquema social inspirado que plantea una analogía entre los conceptos de Justicia de Rawls, Inmanencia de Spinoza, Estado de Hobbes, Paradigma de Kuhn y existencia y esencia de Sartre, abstraídos al plano de virtualización de una red inalámbrica. Cada capa del sistema TLÖN (Figura 1) representa un nivel en la analogía del Estado; inicialmente una capa física del modelo (Territorio) que será una red AdHoc inalámbrica que planteará las condiciones de prestación de los servicios de las capas superiores. La capa de virtualización se puede entender como la función de control que deben ejercer las instituciones de un estado. El concepto de sociedad vendría implícito en la capa del sistema Multiagente, como un conjunto de individuos que interactúan entre sí y con las otras capas del sistema con el fin de prestar y consumir servicios.

Figura 1. Capas del sistema de cómputo TLÖN

![alt text](images/TLON.jpeg)

## SoftTLON

### Procesamiento distribuido - distProc:

Módulo para el procesamiento distribuido a través de una red

Este módulo permite que la distribución de una tarea se ejecute utilizando un conjunto de entradas de datos e imprimiendo todos los resultados en el nodo que inicia el pedido.
  
```PYTHON
importar MultiPManager.distProc
```
  
  
### tlon_parallelize ()
  
Esta función permite ejecutar una función para una matriz de objetos en varias instancias desplegadas a lo largo de la red, estas instancias deben estar previamente suscritas al Tema del recurso y al Tema de órdenes.
Para suscribirse a un cliente, compruebe runclient (int threads).
  
```PYTHON
tlon_parallelize (<ServiceIp>, <Function>, <data_set>)
```
  
La <función> se serializa y comparte con los nodos que están activamente suscritos al tema de los recursos.
El <data_set> está separado en trozos de datos y se cargan en una cola, cada nodo suscrito al orden Topic será entonces un consumidor de la cola de trabajos, ejecutará la <función> compartida en la etapa previa con un fragmento de datos como entrada. El cliente podrá crear tantos hilos como se invocó con (runclient (<ip>, <threads>)) (Nota: Versión 2.0 esto se fusionará con sovora para que las redes Ad-Hoc usen la caracterización de cada nodo )
Después de cada ejecución exitosa de la <Función>, la reanudación se moverá a una cola () que será consumida por el nodo que iniciará el pedido e imprimirá el resultado.
  
### tlon_resources
  
Es un diccionario donde se almacenan todos los recursos compartidos por la red.
Los recursos se comparten con los nodos que están actualmente suscritos a la cola de recursos (</ topic / TLONResources>) en el momento de la publicación.
Nota: La versión 1.1 en adelante tendrá la opción de hacer persistentes estos mensajes para que un consumidor en suscripción reciba todos los mensajes anteriores de un punto en el tiempo, de modo que un consumidor pueda contribuir en una tarea que se esté ejecutando actualmente.
  
## Colas y temas
  
Los recursos y el orden de trabajo (OoW) se compartirán, pensó un corredor de temas, aquí enumeraremos los temas creados para ese propósito:
  
### / topic / TLONResources
Se usa para compartir el recurso agrupado como un mensaje en el intermediario
  
### / topic / TLONOrders
  
Se usa para compartir el orden de trabajo serializado como un mensaje en el intermediario
El orden del trabajo está definido por esta estructura

```PYTHON
OoW =  {
	 "resourceName": <NAME>,
	 "ip": <IP>,
	 "portnum": <MANAGER_PORTNUM>,
	 "authkey": <AUTHKEY>
 }
 ```