.. PtAC documentation master file, created by
   sphinx-quickstart on Fri Jul  9 10:40:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PtAC 0.0.1 alpha
================================

PtAC is a Python library to automatically compute public transport accessbilities for the Sustainable Development Goal 11.2.


Installation 
--------
Installation instructions will be shown here

Features
--------
PtAC is built on top of osmnx, geopandas, networkx and
uses UrMoAC (https://github.com/DLR-VF/UrMoAC) for accessibility computation

* Download and prepare road networks from OpenStreetMap for accessibility calculation
* Calculate accessbilities from origins to the next destination
* Generate a population point dataset from population raster dataset
* Calculate Sustainable Development Goal 11.2 based on starting points with population information


.. toctree::
   :maxdepth: 2
   :caption: User Reference
   
   PtAC


Support
--------


License
--------

The project is licensed under the (XXXMITXXX) license.


Indices 
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
