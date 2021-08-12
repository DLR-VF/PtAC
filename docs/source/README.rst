.. PtAC documentation master file, created by
   sphinx-quickstart on Fri Jul  9 10:40:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PtAC 0.0.3 alpha
----------------

PtAC is a Python package that allows users to automatically compute public transport
accessbilities for the Sustainable Development Goal 11.2. monitored by the proportion
of the population that has convenient access to public transport.
Users can calculate accessibilities from population points to public transit stops
based on maximum distance or - if defined - two different transit systems:
low- and high-capacity.

In order to calculate SDG 11.2.1 indicator the necessary datasets are
population points, public transit stops and city networks.
You can generate population points by converting population rasters (.tif) with
population module. Public transit stops can be obtained from
`OpenStreetMaps (OSM) <https://wiki.openstreetmap.org/wiki/Public_transport>`_ or
`General Transit Feed Specification (GTFS) <https://gtfs.org/>`_ feeds.
If not available, the city network dataset is prepared within the module accessibility
and downloaded as csv.



Getting Started on a windows computer
------------
In order to run the library on a windows computer you have to have a recent python version installed
(we recommend using Anaconda distribution of [python 3.8] https://www.anaconda.com/products/individual ).

**1. open the Anaconda prompt (can be found on windows start menu) and navigate to home folder.

.. code-block:: bash

   cd C:\Users\ptac_user

**2. generate a project folder and navigate to this folder**

.. code-block:: bash
   mkdir ptac
   cd ptac

**3. now, we can create a python virtual environment via conda and**

.. code-block:: bash
   conda create ptac python=3.8

**4. activate the created environment**

.. code-block:: bash
   conda activate ptac

nNw, (ptac) should be displayed in brackets at the starting of the line.

**5. Install necessary libraries**

.. code-block:: bash
   conda install osmnx, rasterio


In order to demonstrate `examples <https://github.com/DLR-VF/PtAC-examples>`_,
jupyter notebook needs to be installed with the following command:

   pip install notebook

For further details see `python packaging instructions
<https://packaging.python.org/tutorials/installing-packages/>`_.

Usage
-----
To get started with PtAC, read the user reference and see sample code and input data in
`examples repository <https://github.com/DLR-VF/PtAC-examples>`_.

Features
--------
PtAC is built on top of osmnx, geopandas, networkx and
uses `UrMoAC <https://github.com/DLR-VF/UrMoAC>`_ for accessibility computation.

* Download and prepare road networks from OpenStreetMap for accessibility calculation
* Calculate accessbilities from origins to the next destination
* Generate a population point dataset from population raster dataset
* Calculate Sustainable Development Goal 11.2 based on starting points with population information

Support
--------

If you have a usage question please contact us via email (simon.nieland@dlr.de,
serra.yosmaoglu@dlr.de).



