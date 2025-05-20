Quick Start
===========

This section demonstrates the basic usage of OpsParser.

Setup and Installation
----------------------

First, install OpsParser using pip:

.. code-block:: bash

   pip install opsparser

Basic Usage Examples
-------------------

Here's a basic example of using OpsParser:

.. code-block:: python

   import openseespy.opensees as ops
   from opsparser import OpenSeesParser
   from opsparser import OpenSeesCommand as Command
   
   # Create a parser instance by passsing OpenSeesPy module object
   parser = OpenSeesParser(ops)
   
   # Hook all OpenSees commands
   parser.hook_all()
   
   # Run OpenSees commands(Anything)
   ops.wipe()
   ops.model("basic", "-ndm", 2, "-ndf", 3)
   ops.node(1, 0.0, 0.0)
   ops.node(2, 1.0, 0.0)

   ops.fix(1, 1, 1, 1)
   ops.mass(2, *[5, 5, 5])

   ops.uniaxialMaterial("Steel01", 1, 420.0, 2E5, 0.01)
   
   # Access parsed data
   Node = Command.NODE.instance
   node_dict = Node.nodes
   
   # Get node coordinates
   coords = Node.get_node_coords(1)
   print(f"Node 1 coordinates: {coords}")
   
   # Clear parser data
   parser.clear()
   
   # Restore original OpenSees functions
   parser.restore_all()