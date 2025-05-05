Elements Module
===============

The Elements Module defines various structural element handlers used in OpenSees. These handlers are responsible for parsing and processing definitions and parameter settings for different types of structural elements.

Zero Length Elements
---------------------

.. py:class:: ZeroLengthHandler

   Handles the creation and parameter setting of zero-length elements.
   
   Zero-length elements are typically used to model springs between nodes, contact conditions, or special boundary conditions.
   
   Supported element types include:
   
   * `ZeroLength <https://openseespydoc.readthedocs.io/en/latest/src/ZeroLength.html>`_ - Standard zero-length element
   * `ZeroLengthSection <https://openseespydoc.readthedocs.io/en/latest/src/zeroLengthSection.html>`_ - Zero-length section element
   * `ZeroLengthND <https://openseespydoc.readthedocs.io/en/latest/src/zeroLengthND.html>`_ - Zero-length element with ND material
   * `ZeroLengthContact2D <https://openseespydoc.readthedocs.io/en/latest/src/zeroLengthContact2D.html>`_ - Zero-length contact element in 2D
   * `ZeroLengthContact3D <https://openseespydoc.readthedocs.io/en/latest/src/zeroLengthContact3D.html>`_ - Zero-length contact element in 3D
   * `CoupledZeroLength <https://openseespydoc.readthedocs.io/en/latest/src/CoupledZeroLength.html>`_ - Coupled zero-length element
   * `ZeroLengthContactNTS2D <https://openseespydoc.readthedocs.io/en/latest/src/ZeroLengthContactNTS2D.html>`_ - Zero-length contact NTS element in 2D
   * `ZeroLengthInterface2D <https://openseespydoc.readthedocs.io/en/latest/src/ZeroLengthInterface2D.html>`_ - Zero-length interface element in 2D
   * `ZeroLengthImpact3D <https://openseespydoc.readthedocs.io/en/latest/src/ZeroLengthImpact3D.html>`_ - Zero-length impact element in 3D

Truss Elements
---------------

.. py:class:: TrussHandler

   Handles the creation and management of truss elements.
   
   Supported element types include:
   
   * `Truss <https://openseespydoc.readthedocs.io/en/latest/src/trussEle.html>`_ - Linear truss element
   * `CorotTruss <https://openseespydoc.readthedocs.io/en/latest/src/corotTruss.html>`_ - Corotational truss element

Beam-Column Elements
--------------------

.. py:class:: BeamColumnHandler

   Handles various beam-column elements.
   
   Supported element types include:
   
   * `ElasticBeamColumn <https://openseespydoc.readthedocs.io/en/latest/src/elasticBeamColumn.html>`_ - Linear elastic beam-column element
   * `DispBeamColumn <https://openseespydoc.readthedocs.io/en/latest/src/dispBeamColumn.html>`_ - Displacement-based beam-column element
   * `ForceBeamColumn <https://openseespydoc.readthedocs.io/en/latest/src/ForceBeamColumn.html>`_ - Force-based beam-column element
   * `NonlinearBeamColumn <https://openseespydoc.readthedocs.io/en/latest/src/nonlinearBeamColumn.html>`_ - Nonlinear beam-column element
   * `DispBeamColumnInt <https://openseespydoc.readthedocs.io/en/latest/src/dispBeamColumn.html>`_ - Displacement-based beam-column element with internal force interpolation
   * `ElasticTimoshenkoBeam <https://openseespydoc.readthedocs.io/en/latest/src/ElasticTimoshenkoBeam.html>`_ - Elastic Timoshenko beam element
   * `ModElasticBeam2d <https://openseespydoc.readthedocs.io/en/latest/src/ModElasticBeam2d.html>`_ - Modified elastic beam element in 2D
   * `BeamWithHinges <https://openseespydoc.readthedocs.io/en/latest/src/BeamWithHinges.html>`_ - Beam with hinges element
   * `FlexShearBeamColumn <https://openseespydoc.readthedocs.io/en/latest/src/FlexShearBeamColumn.html>`_ - Flexure-shear interaction displacement-based beam-column element
   * `MVLEM <https://openseespydoc.readthedocs.io/en/latest/src/MVLEM.html>`_ - Multiple-vertical-line-element-model for RC walls
   * `SFI_MVLEM <https://openseespydoc.readthedocs.io/en/latest/src/SFI_MVLEM.html>`_ - Cyclic shear-flexure interaction model for RC walls
   * `ElasticPipe <https://openseespydoc.readthedocs.io/en/latest/src/ElasticPipe.html>`_ - Elastic pipe element
   * `CurvedPipe <https://openseespydoc.readthedocs.io/en/latest/src/CurvedPipe.html>`_ - Curved pipe element

Joint Elements
----------------

.. py:class:: JointHandler

   Handles joint connection elements.
   
   Mainly used for modeling rigid or semi-rigid behavior of beam-column connections.
   
   Supported element types include:
   
   * `Joint2D <https://openseespydoc.readthedocs.io/en/latest/src/Joint2D.html>`_ - 2D joint element
   * `BeamColumnJoint <https://openseespydoc.readthedocs.io/en/latest/src/beamColumnJoint.html>`_ - Beam-column joint element
   * `ElasticTubularJoint <https://openseespydoc.readthedocs.io/en/latest/src/ElasticTubularJoint.html>`_ - Elastic tubular joint element

Link Elements
--------------

.. py:class:: LinkHandler

   Handles special connection elements.
   
   Includes various types of link elements, such as linear links and nonlinear links.
   
   Supported element types include:
   
   * `TwoNodeLink <https://openseespydoc.readthedocs.io/en/latest/src/twoNodeLink.html>`_ - Two-node link element
   * `MultipleShearSpring <https://openseespydoc.readthedocs.io/en/latest/src/multipleShearSpring.html>`_ - Multiple shear spring element
   * `MultipleNormalSpring <https://openseespydoc.readthedocs.io/en/latest/src/multipleNormalSpring.html>`_ - Multiple normal spring element
   * `KikuchiBearing <https://openseespydoc.readthedocs.io/en/latest/src/KikuchiBearing.html>`_ - Kikuchi bearing element

Bearing Elements
------------------

.. py:class:: BearingHandler

   Handles various bearing elements.
   
   Includes elastic bearings, friction-pendulum bearings, and isolation bearings.
   
   Supported element types include:
   
   * `ElastomericBearingPlasticity <https://openseespydoc.readthedocs.io/en/latest/src/elastomericBearingPlasticity.html>`_ - Elastomeric bearing element with plasticity
   * `ElastomericBearingBoucWen <https://openseespydoc.readthedocs.io/en/latest/src/elastomericBearingBoucWen.html>`_ - Elastomeric bearing element with Bouc-Wen hysteresis
   * `FlatSliderBearing <https://openseespydoc.readthedocs.io/en/latest/src/flatSliderBearing.html>`_ - Flat slider bearing element
   * `SingleFPBearing <https://openseespydoc.readthedocs.io/en/latest/src/singleFPBearing.html>`_ - Single friction pendulum bearing element
   * `ElastomericX <https://openseespydoc.readthedocs.io/en/latest/src/ElastomericX.html>`_ - Elastomeric bearing element with cavitation and post-cavitation
   * `TripleFrictionPendulum <https://openseespydoc.readthedocs.io/en/latest/src/TripleFrictionPendulum.html>`_ - Triple friction pendulum bearing element
   * `TripleFrictionPendulumBearing <https://openseespydoc.readthedocs.io/en/latest/src/TripleFrictionPendulumBearing.html>`_ - Triple friction pendulum bearing element
   * `YamamotoBiaxialHDR <https://openseespydoc.readthedocs.io/en/latest/src/YamamotoBiaxialHDR.html>`_ - Yamamoto biaxial HDR element
   * `LeadRubberX <https://openseespydoc.readthedocs.io/en/latest/src/LeadRubberX.html>`_ - Lead rubber bearing element
   * `HDR <https://openseespydoc.readthedocs.io/en/latest/src/HDR.html>`_ - High damping rubber bearing element
   * `RJWatsonEQS <https://openseespydoc.readthedocs.io/en/latest/src/RJWatsonEQS.html>`_ - RJ-Watson EQS bearing element
   * `FPBearingPTV <https://openseespydoc.readthedocs.io/en/latest/src/FPBearingPTV.html>`_ - Friction pendulum bearing with PTV model

Quadrilateral Elements
------------------------

.. py:class:: QuadrilateralHandler

   Handles two-dimensional quadrilateral elements.
   
   Supported element types include:
   
   * `Quad <https://openseespydoc.readthedocs.io/en/latest/src/quad.html>`_ - Four-node quadrilateral element
   * `ShellMITC4 <https://openseespydoc.readthedocs.io/en/latest/src/ShellMITC4.html>`_ - Four-node MITC shell element
   * `ShellNLDKGQ <https://openseespydoc.readthedocs.io/en/latest/src/ShellNLDKGQ.html>`_ - Four-node shell element with nonlinear drilling DOF
   * `EnhancedQuad <https://openseespydoc.readthedocs.io/en/latest/src/enhancedQuad.html>`_ - Enhanced strain quadrilateral element
   * `ShellDKGQ <https://openseespydoc.readthedocs.io/en/latest/src/ShellDKGQ.html>`_ - Four-node shell element with drilling DOF
   * `BbarPlaneStrain <https://openseespydoc.readthedocs.io/en/latest/src/BbarPlaneStrain.html>`_ - B-bar plane strain quadrilateral element
   * `SSPquad <https://openseespydoc.readthedocs.io/en/latest/src/SSPquad.html>`_ - Stabilized single-point quadrilateral element
   * `MVLEM_3D <https://openseespydoc.readthedocs.io/en/latest/src/MVLEM_3D.html>`_ - 3D multiple-vertical-line-element-model for flexure-dominated RC walls
   * `SFI_MVLEM_3D <https://openseespydoc.readthedocs.io/en/latest/src/SFI_MVLEM_3D.html>`_ - 3D shear-flexure-interaction element for RC walls

Triangular Elements
---------------------

.. py:class:: TriangularHandler

   Handles two-dimensional triangular elements.
   
   Supported element types include:
   
   * `Tri31 <https://openseespydoc.readthedocs.io/en/latest/src/tri31.html>`_ - Three-node triangular element
   * `ShellDKGT <https://openseespydoc.readthedocs.io/en/latest/src/ShellDKGT.html>`_ - Triangular shell element with drilling DOF
   * `ShellNLDKGT <https://openseespydoc.readthedocs.io/en/latest/src/ShellNLDKGT.html>`_ - Triangular shell element with drilling DOF and nonlinear formulation

Brick Elements
----------------

.. py:class:: BrickHandler

   Handles three-dimensional eight-node brick elements.
   
   Commonly used for 3D solid element analysis, supporting behavior analysis under different constitutive models.
   
   Supported element types include:
   
   * `StdBrick <https://openseespydoc.readthedocs.io/en/latest/src/stdBrick.html>`_ - Standard brick element
   * `SSPbrick <https://openseespydoc.readthedocs.io/en/latest/src/SSPbrick.html>`_ - Stabilized Single-Point brick element
   * `BbarBrick <https://openseespydoc.readthedocs.io/en/latest/src/bbarBrick.html>`_ - B-bar brick element
   * `TwentyNodeBrick <https://openseespydoc.readthedocs.io/en/latest/src/20NodeBrick.html>`_ - 20-node brick element
   * `AC3D8 <https://openseespydoc.readthedocs.io/en/latest/src/AC3D8.html>`_ - 8-node brick element for acoustic analysis
   * `ASI3D8 <https://openseespydoc.readthedocs.io/en/latest/src/ASI3D8.html>`_ - 8-node brick element with advanced stress interpolation

Tetrahedron Elements
----------------------

.. py:class:: TetrahedronHandler

   Handles three-dimensional tetrahedral elements.
   
   Suitable for mesh generation and analysis of complex geometric shapes.
   
   Supported element types include:
   
   * `FourNodeTetrahedron <https://openseespydoc.readthedocs.io/en/latest/src/FourNodeTetrahedron.html>`_ - Four-node tetrahedral element
   * `TenNodeTetrahedron <https://openseespydoc.readthedocs.io/en/latest/src/TenNodeTetrahedron.html>`_ - Ten-node tetrahedral element
   * `VS3D4 <https://openseespydoc.readthedocs.io/en/latest/src/VS3D4.html>`_ - Four-node tetrahedral element for vibration and seismic analysis

UCSD UP Elements
------------------

.. py:class:: UCSDUpHandler

   Handles u-p elements developed by the University of California, San Diego.
   
   Mainly used for excess pore water pressure analysis and liquefaction dynamic analysis.
   
   Supported element types include:
   
   * `NineFourNodeQuadUP <https://openseespydoc.readthedocs.io/en/latest/src/NineFourNodeQuadUP.html>`_ - 9-4-quad u-p element (9 nodes for displacement, 4 for pressure)
   * `TwentyEightNodeBrickUP <https://openseespydoc.readthedocs.io/en/latest/src/TwentyEightNodeBrickUP.html>`_ - 20-8-brick u-p element (20 nodes for displacement, 8 for pressure)

Other UP Elements
-------------------

.. py:class:: OtherUpHandler

   Handles u-p elements not developed by UCSD.
   
   Includes various special types of u-p element implementations.
   
   Supported element types include:
   
   * `BrickUP <https://openseespydoc.readthedocs.io/en/latest/src/brickUP.html>`_ - 8-node brick u-p element
   * `QuadUP <https://openseespydoc.readthedocs.io/en/latest/src/quadUP.html>`_ - 4-node quad u-p element
   * `SSPquadUP <https://openseespydoc.readthedocs.io/en/latest/src/SSPquadUP.html>`_ - Stabilized single-point quad u-p element
   * `SSPbrickUP <https://openseespydoc.readthedocs.io/en/latest/src/SSPbrickUP.html>`_ - Stabilized single-point brick u-p element

Contact Elements
-------------------

.. py:class:: ContactHandler

   Handles contact relationships between nodes or elements.
   
   Supported element types include:
   
   * `SimpleContact2D <https://openseespydoc.readthedocs.io/en/latest/src/SimpleContact2D.html>`_ - Simple contact element in 2D
   * `SimpleContact3D <https://openseespydoc.readthedocs.io/en/latest/src/SimpleContact3D.html>`_ - Simple contact element in 3D
   * `BeamContact2D <https://openseespydoc.readthedocs.io/en/latest/src/BeamContact2D.html>`_ - Beam-to-node contact element in 2D
   * `BeamContact3D <https://openseespydoc.readthedocs.io/en/latest/src/BeamContact3D.html>`_ - Beam-to-node contact element in 3D
   * `BeamEndContact3D <https://openseespydoc.readthedocs.io/en/latest/src/BeamEndContact3D.html>`_ - Beam end contact element in 3D

Cable Elements
----------------

.. py:class:: CableHandler

   Handles flexible cable elements.
   
   Mainly used for modeling suspension bridges, cable systems, and other cable structures.
   
   Supported element types include:
   
   * `CatenaryCable <https://openseespydoc.readthedocs.io/en/latest/src/CatenaryCable.html>`_ - Catenary cable element

PFEM Elements
---------------

.. py:class:: PFEMHandler

   Handles Particle Finite Element Method elements.
   
   Used for fluid-structure interaction and large deformation problems.
   
   Supported element types include:
   
   * `PFEMElementBubble <https://openseespydoc.readthedocs.io/en/latest/src/PFEMElementBubble.html>`_ - 2D PFEM element
   * `PFEMElementCompressible <https://openseespydoc.readthedocs.io/en/latest/src/PFEMElementCompressible.html>`_ - Compressible PFEM element

Miscellaneous Elements
-----------------------

.. py:class:: MiscHandler

   Handles other special elements that don't belong to the above categories.
   
   Includes various special element types and their implementations, such as:
   
   * `SurfaceLoad <https://openseespydoc.readthedocs.io/en/latest/src/SurfaceLoad.html>`_ - Surface load element
   * `VS3D4 <https://openseespydoc.readthedocs.io/en/latest/src/VS3D4.html>`_ - Four-node tetrahedral element for vibration and seismic analysis
   * `AC3D8 <https://openseespydoc.readthedocs.io/en/latest/src/AC3D8.html>`_ - 8-node brick element for acoustic analysis
   * `ASI3D8 <https://openseespydoc.readthedocs.io/en/latest/src/ASI3D8.html>`_ - 8-node brick element with advanced stress interpolation
   * `AV3D4 <https://openseespydoc.readthedocs.io/en/latest/src/AV3D4.html>`_ - 4-node acoustic-vibration tetrahedral element
   * `MasonPan12 <https://openseespydoc.readthedocs.io/en/latest/src/MasonPan12.html>`_ - 12-node Masonry panel element