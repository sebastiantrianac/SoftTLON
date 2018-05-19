# TLON

Volante Monitor is a Designer modules (from Designer version >= 5.1.3 ) thought as a REStFUL integration framework.
Simply put the volanteMonitor cartridge as a dependency in any final designer project and:
* It can help an integrator to publish some DataBase resources through both Facade, jQuery DataTable or any specific pattern relying on any view/model based integration.
* Unless you have any specific service publication or implementation needs, you do not have to generate your own REStFUL path's in order to publish any CRUDS and jQuery DataTables based reports. These ones will already be available for the end applications.

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
