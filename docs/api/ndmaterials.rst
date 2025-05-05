ND Materials Module
======================

The ND Materials Module defines various multi-dimensional material model handlers used in OpenSees. These handlers are responsible for parsing and processing definitions and parameter settings for different types of multi-dimensional materials.

Standard Models
-----------------------

.. py:class:: NDMaterialHandler

   Handles standard multi-dimensional material models.
   
   Supported material types include:
   
   * `ElasticIsotropic <https://openseespydoc.readthedocs.io/en/latest/src/elasticIsotropic.html>`_ - Elastic isotropic material
   * `ElasticOrthotropic <https://openseespydoc.readthedocs.io/en/latest/src/elasticOrthotropic.html>`_ - Elastic orthotropic material
   * `J2Plasticity <https://openseespydoc.readthedocs.io/en/latest/src/J2Plasticity.html>`_ - J2 plasticity material
   * `DruckerPrager <https://openseespydoc.readthedocs.io/en/latest/src/DrunkerPrager.html>`_ - Drucker-Prager plasticity material
   * `PlaneStress <https://openseespydoc.readthedocs.io/en/latest/src/PlaneStress.html>`_ - Plane stress material
   * `PlaneStrain <https://openseespydoc.readthedocs.io/en/latest/src/PlaneStrain.html>`_ - Plane strain material
   * `MultiaxialCyclicPlasticity <https://openseespydoc.readthedocs.io/en/latest/src/MultiAxialCyclicPlasticity.html>`_ - Multiaxial cyclic plasticity material
   * `BoundingCamClay <https://openseespydoc.readthedocs.io/en/latest/src/BoundingCamClay.html>`_ - Bounding Cam Clay material
   * `PlateFiber <https://openseespydoc.readthedocs.io/en/latest/src/PlateFiber.html>`_ - Plate fiber material
   * `FSAM <https://openseespydoc.readthedocs.io/en/latest/src/FSAM.html>`_ - Fixed-strut-angle model
   * `ManzariDafalias <https://openseespydoc.readthedocs.io/en/latest/src/ManzariDafalias.html>`_ - Manzari-Dafalias material
   * `PM4Sand <https://openseespydoc.readthedocs.io/en/latest/src/PM4Sand.html>`_ - PM4Sand material
   * `PM4Silt <https://openseespydoc.readthedocs.io/en/latest/src/PM4Silt.html>`_ - PM4Silt material
   * `StressDensityModel <https://openseespydoc.readthedocs.io/en/latest/src/StressDensityModel.html>`_ - Stress density model
   * `AcousticMedium <https://openseespydoc.readthedocs.io/en/latest/src/AcousticMedium.html>`_ - Acoustic medium material

Tsinghua Sand Models
-------------------------

.. py:class:: TsinghuaSandModelsHandler

   Handles sand constitutive models developed by Tsinghua University.
   
   Suitable for simulating and analyzing various sand foundations.
   
   Supported material types include:
   
   * `CycLiqCP <https://openseespydoc.readthedocs.io/en/latest/src/CycLiqCP.html>`_ - Cyclic liquefaction material
   * `CycLiqCPSP <https://openseespydoc.readthedocs.io/en/latest/src/CycLiqCPSP.html>`_ - Cyclic liquefaction material with shear-induced pore pressure

Materials for Modeling Concrete Walls
-----------------------------------------

.. py:class:: ConcreteWallsHandler

   Handles specialized material models for concrete walls.
   
   Supported material types include:
   
   * `PlateFromPlaneStress <https://openseespydoc.readthedocs.io/en/latest/src/PlateFromPlaneStress.html>`_ - Plate from plane stress material
   * `PlateRebar <https://openseespydoc.readthedocs.io/en/latest/src/PlateRebar.html>`_ - Plate rebar material
   * `PlasticDamageConcretePlaneStress <https://openseespydoc.readthedocs.io/en/latest/src/PlasticDamageConcretePlaneStress.html>`_ - Plastic damage concrete plane stress material

Contact Materials for 2D and 3D
--------------------------------

.. py:class:: ContactMaterialsHandler

   Handles contact relationship models between structural elements.
   
   Includes various contact models such as surface contact and frictional contact.
   
   Supported material types include:
   
   * `ContactMaterial2D <https://openseespydoc.readthedocs.io/en/latest/src/ContactMaterial2D.html>`_ - 2D contact material
   * `ContactMaterial3D <https://openseespydoc.readthedocs.io/en/latest/src/ContactMaterial3D.html>`_ - 3D contact material

Wrapper material for Initial State Analysis
--------------------------------------------

.. py:class:: InitialStateHandler

   Handles setting initial stress and strain states for materials.
   
   Applicable to analyses that need to consider prestressing or initial strains.
   
   Supported material types include:
   
   * `InitialStateAnalysisWrapper <https://openseespydoc.readthedocs.io/en/latest/src/InitialStateAnalysisWrapper.html>`_ - Initial state material wrapper
   * `InitStressNDMaterial <https://openseespydoc.readthedocs.io/en/latest/src/InitStressNDMaterial.html>`_ - Initial Stress Material
   * `InitStrainNDMaterial <https://openseespydoc.readthedocs.io/en/latest/src/InitStrainNDMaterial.html>`_ - Initial Strain Material

UC San Diego soil models
-------------------------

.. py:class:: UCSDSoilModelsHandler

   Handles general soil models developed by the University of California, San Diego.
   
   Includes a series of constitutive models suitable for different soil types.
   
   Supported material types include:
   
   * `PressureIndependMultiYield <https://openseespydoc.readthedocs.io/en/latest/src/PressureIndependMultiYield.html>`_ - Pressure-independent multi-yield surface clay material
   * `PressureDependMultiYield <https://openseespydoc.readthedocs.io/en/latest/src/PressureDependMultiYield.html>`_ - Pressure-dependent multi-yield surface clay material
   * `PressureDependMultiYield02 <https://openseespydoc.readthedocs.io/en/latest/src/PressureDependMultiYield02.html>`_ - Pressure-dependent multi-yield surface material for sand
   * `PressureDependMultiYield03 <https://openseespydoc.readthedocs.io/en/latest/src/PressureDependMultiYield03.html>`_ - Improved pressure-dependent multi-yield surface material for clay

UC San Diego Saturated Undrained soil
--------------------------------------

.. py:class:: UCSDSaturatedSoilHandler

   Handles saturated soil models developed by the University of California, San Diego.
   
   Suitable for soil analyses that consider pore water pressure.
   
   Supported material types include:
   
   * `FluidSolidPorousMaterial <https://openseespydoc.readthedocs.io/en/latest/src/FluidSolidPorousMaterial.html>`_ - Fluid-solid porous material
