Uniaxial Materials Module
============================

The Uniaxial Materials Module defines various uniaxial material model handlers used in OpenSees. These handlers are responsible for parsing and processing definitions and parameter settings for different types of uniaxial materials.

Steel & Reinforcing-Steel Materials
--------------------------------------

.. py:class:: SteelReinforcingHandler

   Handles various steel and reinforcing steel material models.
   
   Supported material types include:
   
   * `Steel01 <https://openseespydoc.readthedocs.io/en/latest/src/steel01.html>`_ - Bilinear steel material
   * `Steel02 <https://openseespydoc.readthedocs.io/en/latest/src/steel02.html>`_ - Giuffré-Menegotto-Pinto steel material with isotropic hardening
   * `Steel4 <https://openseespydoc.readthedocs.io/en/latest/src/steel4.html>`_ - Comprehensive uniaxial Giuffré-Menegotto-Pinto steel material
   * `ReinforcingSteel <https://openseespydoc.readthedocs.io/en/latest/src/ReinforcingSteel.html>`_ - Reinforcing steel material with buckling and fatigue
   * `Dodd_Restrepo <https://openseespydoc.readthedocs.io/en/latest/src/Dodd_Restrepo.html>`_ - Dodd-Restrepo steel material model
   * `RambergOsgoodSteel <https://openseespydoc.readthedocs.io/en/latest/src/RambergOsgoodSteel.html>`_ - Ramberg-Osgood steel material
   * `SteelMPF <https://openseespydoc.readthedocs.io/en/latest/src/SteelMPF.html>`_ - Multi-point form of Steel material
   * `Steel01Thermal <https://openseespydoc.readthedocs.io/en/latest/src/steel01thermal.html>`_ - Temperature-dependent version of Steel01

Concrete Materials
-------------------

.. py:class:: ConcreteHandler

   Handles various concrete material models, including standard concrete models and high-performance concrete.
   
   Supported material types include:
   
   * `Concrete01 <https://openseespydoc.readthedocs.io/en/latest/src/Concrete01.html>`_ - Basic concrete material with linear tension softening
   * `Concrete02 <https://openseespydoc.readthedocs.io/en/latest/src/Concrete02.html>`_ - Concrete material with linear tension softening and nonlinear compression
   * `Concrete04 <https://openseespydoc.readthedocs.io/en/latest/src/Concrete04.html>`_ - Popovics concrete material
   * `Concrete06 <https://openseespydoc.readthedocs.io/en/latest/src/Concrete06.html>`_ - Concrete material based on Thorenfeldt curve
   * `Concrete07 <https://openseespydoc.readthedocs.io/en/latest/src/Concrete07.html>`_ - Chang & Mander's 1994 concrete model
   * `Concrete01WithSITC <https://openseespydoc.readthedocs.io/en/latest/src/Concrete01WithSITC.html>`_ - Concrete01 with strain-independent tension cutoff
   * `ConfinedConcrete01 <https://openseespydoc.readthedocs.io/en/latest/src/ConfinedConcrete01.html>`_ - Confined concrete model
   * `ConcreteD <https://openseespydoc.readthedocs.io/en/latest/src/ConcreteD.html>`_ - Damage-based concrete model
   * `FRPConfinedConcrete <https://openseespydoc.readthedocs.io/en/latest/src/FRPConfinedConcrete.html>`_ - FRP-confined concrete material
   * `FRPConfinedConcrete02 <https://openseespydoc.readthedocs.io/en/latest/src/FRPConfinedConcrete02.html>`_ - FRP-confined concrete material (improved)
   * `ConcreteCM <https://openseespydoc.readthedocs.io/en/latest/src/ConcreteCM.html>`_ - Comprehensive concrete material model
   * `TDConcrete <https://openseespydoc.readthedocs.io/en/latest/src/TDConcrete.html>`_ - Time-dependent concrete material
   * `TDConcreteEXP <https://openseespydoc.readthedocs.io/en/latest/src/TDConcreteEXP.html>`_ - Time-dependent concrete material with explicit form
   * `TDConcreteMC10 <https://openseespydoc.readthedocs.io/en/latest/src/TDConcreteMC10.html>`_ - Time-dependent concrete material based on Model Code 2010
   * `TDConcreteMC10NL <https://openseespydoc.readthedocs.io/en/latest/src/TDConcreteMC10NL.html>`_ - Time-dependent concrete material with nonlinear creep based on Model Code 2010

Standard Uniaxial Materials
-----------------------------

.. py:class:: StandardUniaxialHandler

   Specialized handler for uniaxial material models.
   
   Supported material types include:
   
   * `Elastic Uniaxial Material <https://openseespydoc.readthedocs.io/en/latest/src/ElasticUni.html>`_ - Linear elastic material
   * `Elastic-Perfectly Plastic Material <https://openseespydoc.readthedocs.io/en/latest/src/ElasticPP.html>`_ - Elastic-perfectly plastic material
   * `Elastic-Perfectly Plastic Gap Material <https://openseespydoc.readthedocs.io/en/latest/src/ElasticPPGap.html>`_ - Elastic-perfectly plastic gap material
   * `Elastic-No Tension Material <https://openseespydoc.readthedocs.io/en/latest/src/ENT.html>`_ - Elastic-no tension material
   * `Hysteretic <https://openseespydoc.readthedocs.io/en/latest/src/Hysteretic.html>`_ - Hysteretic material for modeling pinching and degradation
   * `Parallel Material <https://openseespydoc.readthedocs.io/en/latest/src/ParallelUni.html>`_ - Parallel material for combining materials in parallel
   * `Series Material <https://openseespydoc.readthedocs.io/en/latest/src/SeriesUni.html>`_ - Series material for combining materials in series

PyTzQz uniaxial materials for p-y, t-z and q-z elements for modeling soil-structure interaction
------------------------------------------------------------------------------------------------

.. py:class:: PyTzQzHandler

   Specialized material handler for soil-pile interaction models.
   
   Includes:
   
   * `PySimple1 Material <https://openseespydoc.readthedocs.io/en/latest/src/PySimple1.html>`_ - Lateral soil-pile p-y material
   * `TzSimple1 Material <https://openseespydoc.readthedocs.io/en/latest/src/TzSimple1.html>`_ - Vertical soil-pile t-z material
   * `QzSimple1 Material <https://openseespydoc.readthedocs.io/en/latest/src/QzSimple1.html>`_ - Pile tip soil q-z material
   * `PyLiq1 Material <https://openseespydoc.readthedocs.io/en/latest/src/PyLiq1.html>`_ - PySimple1 with liquefaction effects
   * `TzLiq1 Material <https://openseespydoc.readthedocs.io/en/latest/src/TzLiq1.html>`_ - TzSimple1 with liquefaction effects
   * `QzLiq1 Material <https://openseespydoc.readthedocs.io/en/latest/src/QzLiq1.html>`_ - QzSimple1 with liquefaction effects

Other Uniaxial Materials
--------------------------

.. py:class:: OtherUniaxialHandler

   Handles specialized uniaxial material models that don't fit into the above categories.
   
   Includes various special-purpose uniaxial material models such as:
   
   * `Hardening Material <https://openseespydoc.readthedocs.io/en/latest/src/Hardening.html>`_ - Hardening material
   * `CastFuse Material <https://openseespydoc.readthedocs.io/en/latest/src/Cast.html>`_ - Cast fuse material
   * `ViscousDamper Material <https://openseespydoc.readthedocs.io/en/latest/src/ViscousDamper.html>`_ - Viscous damper material
   * `BilinearOilDamper Material <https://openseespydoc.readthedocs.io/en/latest/src/BilinearOilDamper.html>`_ - Bilinear oil damper material
   * `Modified Ibarra-Medina-Krawinkler Deterioration Model with Bilinear Hysteretic Response (Bilin Material) <https://openseespydoc.readthedocs.io/en/latest/src/Bilin.html>`_ - Bilinear material with degradation
   * `Modified Ibarra-Medina-Krawinkler Deterioration Model with Peak-Oriented Hysteretic Response (ModIMKPeakOriented Material) <https://openseespydoc.readthedocs.io/en/latest/src/ModIMKPeakOriented.html>`_ - Peak-oriented hysteretic response material
   * `Modified Ibarra-Medina-Krawinkler Deterioration Model with Pinched Hysteretic Response (ModIMKPinching Material) <https://openseespydoc.readthedocs.io/en/latest/src/ModIMKPinching.html>`_ - Pinched hysteretic response material
   * `SAWS Material <https://openseespydoc.readthedocs.io/en/latest/src/SAWS.html>`_ - SAWS material
   * `BarSlip Material <https://openseespydoc.readthedocs.io/en/latest/src/BarSlip.html>`_ - Bar slip material
   * `Bond SP01 - - Strain Penetration Model for Fully Anchored Steel Reinforcing Bars <https://openseespydoc.readthedocs.io/en/latest/src/Bond_SP01.html>`_ - Bond strain penetration model
   * `Fatigue Material <https://openseespydoc.readthedocs.io/en/latest/src/Fatigue.html>`_ - Fatigue material
   * `Impact Material <https://openseespydoc.readthedocs.io/en/latest/src/ImpactMaterial.html>`_ - Impact material
   * `Hyperbolic Gap Material <https://openseespydoc.readthedocs.io/en/latest/src/HyperbolicGapMaterial.html>`_ - Hyperbolic gap material
   * `Limit State Material <https://openseespydoc.readthedocs.io/en/latest/src/LimitState.html>`_ - Limit state material
   * `MinMax Material <https://openseespydoc.readthedocs.io/en/latest/src/MinMax.html>`_ - Min-max material
   * `ElasticBilin Material <https://openseespydoc.readthedocs.io/en/latest/src/ElasticBilin.html>`_ - Elastic bilinear material
   * `ElasticMultiLinear Material <https://openseespydoc.readthedocs.io/en/latest/src/ElasticMultiLinear.html>`_ - Elastic multi-linear material
   * `MultiLinear <https://openseespydoc.readthedocs.io/en/latest/src/MultiLinear.html>`_ - Multilinear material
   * `Initial Strain Material <https://openseespydoc.readthedocs.io/en/latest/src/InitStrainMaterial.html>`_ - Initial strain material
   * `Initial Stress Material <https://openseespydoc.readthedocs.io/en/latest/src/InitStressMaterial.html>`_ - Initial stress material
   * `PathIndependent Material <https://openseespydoc.readthedocs.io/en/latest/src/PathIndependent.html>`_ - Path independent material
   * `Pinching4 Material <https://openseespydoc.readthedocs.io/en/latest/src/Pinching4.html>`_ - Pinching4 material
   * `Engineered Cementitious Composites Material <https://openseespydoc.readthedocs.io/en/latest/src/ECC01.html>`_ - ECC material
   * `SelfCentering Material <https://openseespydoc.readthedocs.io/en/latest/src/SelfCentering.html>`_ - Self-centering material
   * `Viscous Material <https://openseespydoc.readthedocs.io/en/latest/src/Viscous.html>`_ - Viscous material
   * `BoucWen Material <https://openseespydoc.readthedocs.io/en/latest/src/BoucWen.html>`_ - Bouc-Wen hysteretic material
   * `BWBN Material <https://openseespydoc.readthedocs.io/en/latest/src/BWBN.html>`_ - BWBN material
   * `KikuchiAikenHDR Material <https://openseespydoc.readthedocs.io/en/latest/src/KikuchiAikenHDR.html>`_ - Kikuchi-Aiken HDR material
   * `KikuchiAikenLRB Material <https://openseespydoc.readthedocs.io/en/latest/src/KikuchiAikenLRB.html>`_ - Kikuchi-Aiken LRB material
   * `AxialSp Material <https://openseespydoc.readthedocs.io/en/latest/src/AxialSp.html>`_ - Axial Sp material
   * `AxialSpHD Material <https://openseespydoc.readthedocs.io/en/latest/src/AxialSpHD.html>`_ - Axial Sp HD material
   * `Pinching Limit State Material <https://openseespydoc.readthedocs.io/en/latest/src/PinchingLimitStateMaterial.html>`_ - Pinching limit state material
   * `CFSWSWP Wood-Sheathed Cold-Formed Steel Shear Wall Panel <https://openseespydoc.readthedocs.io/en/latest/src/CFSWSWP.html>`_ - Wood-sheathed CFS shear wall panel
   * `CFSSSWP Steel-Sheathed Cold-formed Steel Shear Wall Panel <https://openseespydoc.readthedocs.io/en/latest/src/CFSSSWP.html>`_ - Steel-sheathed CFS shear wall panel
   * `Backbone Material <https://openseespydoc.readthedocs.io/en/latest/src/Backbone.html>`_ - Backbone material
   * `Masonry <https://openseespydoc.readthedocs.io/en/latest/src/Masonry.html>`_ - Masonry material
   * `Pipe Material <https://openseespydoc.readthedocs.io/en/latest/src/pipeMaterial.html>`_ - Pipe material
