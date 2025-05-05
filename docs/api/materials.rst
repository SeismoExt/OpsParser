Materials Module
=================

The Materials Module defines various material model handlers used in OpenSees. These handlers are responsible for parsing and processing definitions and parameter settings for different types of materials.

Materials have been separated into two categories:

.. toctree::
   :maxdepth: 2
   
   uniaxialmaterials
   ndmaterials

Uniaxial Materials
-----------------------

Uniaxial materials are one-dimensional and typically used in truss elements, zero-length elements, and as fibers in sections. See the :doc:`uniaxialmaterials` documentation for detailed information on the following handlers:

* **ConcreteHandler** - Handles concrete material models (Concrete01, Concrete02, etc.)
* **ConcreteWallsHandler** - Specialized for concrete walls
* **StandardUniaxialHandler** - Handles standard uniaxial materials (Elastic, ElasticPP, etc.)
* **SteelReinforcingHandler** - Handles steel material models (Steel01, Steel02, etc.)
* **PyTzQzHandler** - Specialized for soil-pile interface materials
* **StandardModelsHandler** - Handles various standard uniaxial material models
* **OtherUniaxialHandler** - Handles other specialized uniaxial materials

ND Materials
--------------

ND (multi-dimensional) materials are used in continuum elements and certain specialized elements. See the :doc:`ndmaterials` documentation for detailed information on the following handlers:

* **UCSDSaturatedSoilHandler** - Handles saturated soil models from UCSD
* **UCSDSoilModelsHandler** - Handles general soil models from UCSD
* **TsinghuaSandModelsHandler** - Handles sand models from Tsinghua University
* **NDMaterialHandler** - Handles standard multi-dimensional materials
* **ContactMaterialsHandler** - Handles contact materials
* **InitialStateHandler** - Handles materials with initial stress/strain states