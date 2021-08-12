
PtAC 0.0.3 alpha
----------------

PtAC is a Python package to automatically compute walking
accessibilities from residential areas to public transport stops for the Sustainable Development Goal 11.2
defined by the United Nations. The goal aims to measure and monitor the proportion
of the population in a city that has convenient access to public transport
(see https://sdgs.un.org/goals/goal11). With this library users can download and process `OpenStreetMaps <https://www.openstreetmap.org>`_ (OSM)
street networks and population information worldwide. Based on this it is possible to calculate accessibilities
from population points to public transit stops based on minimum street network distance.

In order to calculate SDG 11.2.1 indicator the necessary input sources are
population information, public transit stops and city networks.
Worldwide population information can be downloaded via WMS from 
`World Settlement Footprint <https://figshare.com/articles/dataset/World_Settlement_Footprint_WSF_2015/10048412>`_
(WSF) and converted
to points. Public transit stops can be obtained from
OpenStreetMaps (OSM) (https://wiki.openstreetmap.org/wiki/Public_transport) or
General Transit Feed Specification (GTFS) (https://gtfs.org/) feeds (have a look at the examples if you want to know how this
works exactly). The street network can be downloaded and prepared for routing automatically within the library.



Getting Started
------------
In order to run the library on a windows computer you have to have a recent python version installed
(we recommend using Anaconda distribution of [python 3.8] https://www.anaconda.com/products/individual ).

**1. open the Anaconda prompt (can be found on windows start menu) and navigate to your home folder**

.. code-block:: bash

   cd C:\Users\ptac_user

**2. generate a project folder and navigate to this folder**

.. code-block:: bash

   mkdir ptac
   cd ptac

**3. now, we can create a python virtual environment via conda and activate the created environment**

.. code-block:: bash

   conda create ptac python=3.8
   conda activate ptac

(ptac) should now be displayed in brackets at the starting of the line.

**4. in the next step, install necessary dependency libraries**

.. code-block:: bash

   conda install osmnx, rasterio

**5. you are able to install ptac now by typing**

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ ptac



In order to try out the `examples <https://github.com/DLR-VF/PtAC-examples>`_,
jupyter notebook needs to be installed with the following command:

.. code-block:: bash
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



