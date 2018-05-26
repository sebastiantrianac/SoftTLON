# TLON

TLÖN es un sistema de cómputo propuesto por el grupo de investigación en redes de Telecomunicaciones Dinámicas y lenguajes de programación distribuidos de la Universidad Nacional de Colombia. El modelo que propone TLÖN es un esquema social inspirado que plantea una analogía entre los conceptos de Justicia de Rawls, Inmanencia de Spinoza, Estado de Hobbes, Paradigma de Kuhn y existencia y esencia de Sartre, abstraídos al plano de virtualización de una red inalámbrica. Cada capa del sistema TLÖN (Figura 1) representa un nivel en la analogía del Estado; inicialmente una capa física del modelo (Territorio) que será una red AdHoc inalámbrica que planteará las condiciones de prestación de los servicios de las capas superiores. La capa de virtualización se puede entender como la función de control que deben ejercer las instituciones de un estado. El concepto de sociedad vendría implícito en la capa del sistema Multiagente, como un conjunto de individuos que interactúan entre sí y con las otras capas del sistema con el fin de prestar y consumir servicios.

Figura 1. Capas del sistema de cómputo TLÖN

![alt text](images/TLON.jpeg)

## SoftTLON

### Distributed Processing - distProc:

Module for distributed processing over a network

This module allows the distribution of a task to be run using a set of data inputs and printing all the results at the node that starts the Order.

```PYTHON
import MultiPManager.distProc
```


### tlon_parallelize()

This function allows to execute a function for an array of objects across multiple instances deployed along the network, this instances have to been previously subscribed to the resource Topic and the Orders Topic.
To subscribe a client please check runclient(int threads).

```PYTHON
tlon_parallelize(<ServiceIp>, <Function>, <data_set>)
```

The <function> is serialized and shared with the nodes that are actively subscribed to the topic of resources.
The <data_set> is separated in chunks of data an are load to a queue, every node subscribed to the order Topic will then be a consumer of the queue of jobs, it will execute the <function> shared in the previous stage with a chunk of data as input. The client will be able to create as many threads as it was invoked with (runclient(<ip>,<threads>)) (Note: Version 2.0 this will be merged with sovora for Ad-Hoc networks to use the characterization of each node).
After each successful execution of the <Function> the resoult will be moved to a queue () which its going to be consumed by the node that start the order and print the result.

### tlon_resources

Is a dictionary where is stored all the resources shared by the network.
The resources are shared to the nodes that currently are subscribed to the resource queue (</topic/TLONResources>) at the moment of posting.
Note: Version 1.1 onwards will have the option to make persistent this messages so a consumer at subscription will receive all previous messages from a point in time, so in that way a consumer can contribute at a currently executing task.

## Queues and Topics

The resources and order of Work (OoW) will be shared thought a broker of Topics, here we'll list the topics created for that purpose:

### /topic/TLONResources
Used for sharing the marshalled resource as a message in the broker

### /topic/TLONOrders

Used for sharing the serialized Order of Work as a message in the broker
The order of Work are defined by this structure

```PYTHON
OoW =  {
        "resourceName": <name>,
        "ip": <IP>,
        "portnum": <MANAGER_PORTNUM>,
        "authkey": <AUTHKEY>
        }
```
----

