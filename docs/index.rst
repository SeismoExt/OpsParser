.. This theme is based on the `sphinx-needs`.

.. grid::
   :gutter: 2 3 3 3
   :margin: 4 4 1 2
   :class-container: architecture-bg
   :class-row: sd-w-100

   .. grid-item::
      :columns: auto
      :child-align: justify
      :class: sd-fs-3

      .. div:: sd-font-weight-bold
         
         Recording OpenSeesPy Commands easily & effortlessly

      .. div:: sd-fs-5 sd-font-italic

         Welcome to the documentation for OpenSeesParser(OpsParser), a package designed for spying on any OpenSeesPy scripts.
         OpsParser is a tool for analyzing and processing OpenSees commands. It provides a flexible API for parsing, monitoring, 
         and manipulating the execution of OpenSees commands. With this tool, you can easily track every OpenSeesPy command 
         and perform various operations based on these records.

      .. grid:: 1 1 2 2
         :gutter: 2 2 3 3
         :margin: 0
         :padding: 0

         .. grid-item::
            :columns: auto

            .. button-ref:: quick_start
               :ref-type: doc
               :outline:
               :color: primary
               :class: sd-rounded-pill sd-px-4 sd-fs-5

               Get Started
      
         .. grid-item::
            :columns: auto

            .. button-link:: https://opensees.berkeley.edu/
               :outline:
               :color: primary
               :class: sd-rounded-pill sd-px-4 sd-fs-5

               OpenSees
         
         .. grid-item::
            :columns: auto

            .. button-link:: https://openseespydoc.readthedocs.io/en/latest/index.html#
               :outline:
               :color: primary
               :class: sd-rounded-pill sd-px-4 sd-fs-5

               OpenSeesPy
         
         .. grid-item::
            :columns: auto

            .. button-link:: https://opstool.readthedocs.io/en/stable/index.html
               :outline:
               :color: primary
               :class: sd-rounded-pill sd-px-4 sd-fs-5

               Opstool

------------------------------------------------------------------------------------------------------

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :octicon:`shield-check;1.5em;sd-mr-1 fill-primary` Ultra-lightweight

      - No third-party library dependencies
      - Pure Python implementation, easy installation
      - Minimal memory footprint
      - Efficient command capturing mechanism
      - Compatible with any OpenSeesPy version
      - No impact on original OpenSees performance
  
   .. grid-item-card:: :octicon:`checkbox;1.5em;sd-mr-1 fill-primary` API Support

      As a flexible command monitoring tool, OpsParser can be easily integrated into other services,
      TODO: providing standardized API interfaces that allow third-party applications to access OpenSees command 
      TODO: execution information in real-time, supporting custom processing workflows and event triggering mechanisms.


Contents
----------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   installation.rst
   quick_start.rst
   known_issues.rst

.. toctree::  
   :maxdepth: 2  
   :caption: Documentation:  
  
   examples/index.ipynb
   api/index  

Indices and Tables
====================
  
* :ref:`genindex`  
* :ref:`modindex`  
* :ref:`search`


