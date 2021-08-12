.. PtAC documentation master file, created by
   sphinx-quickstart on Fri Jul  9 10:40:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PtAC 0.0.3 alpha
----------------

PtAC is a Python package to automatically compute walking
accessbilities from residential areas to public transport stops for the Sustainable Development Goal 11.2
defined by the United Nations. The goal aims to measure and monitor the proportion
of the population in a city that has convenient access to public transport
(see [sdg 11.2.1] https://sdgs.un.org/goals/goal11). With this library users can download and process OSM
street networks and population information worldwide. Based on this it is possible to calculate accessibilities
from population points to public transit stops based on minimum street network distance.

In order to calculate SDG 11.2.1 indicator the necessary input sources are
population information, public transit stops and city networks.
Worldwide population information can be downloaded via WMS from [Word settlement footprint] https://insert_link and converted
to points. Public transit stops can be obtained from
[OpenStreetMaps (OSM)](https://wiki.openstreetmap.org/wiki/Public_transport) or
[General Transit Feed Specification (GTFS)](https://gtfs.org/) feeds (have a look at the examples if you want to know how this
works exactly). The street network can be downloaded and prepared for routing automatically within the library.



(Windows) Installation
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



There are certain packages are required to be installed before using the package. This is a bit tricky on windows,
therefore it is important to do everything in the specified order.

Windows users should download the following binaries into the project folder (C:\Users\ptac_user\ptac)
from `Unofficial Windows Binaries for Python Extension Packages
<https://www.lfd.uci.edu/~gohlke/pythonlibs/>`_:
GDAL, Pyproj (v3.1.0), Fiona, Shapely (v1.7.1) and Geopandas (v0.9.0)
in the correct version of Python
and operating system (32-bit or 64-bit) is installed on the computer
(e.g. for Python version 3.9x (64-bit), GDAL-3.3.1-cp39-cp39-win_amd64.whl should be installed).
The following order of installation is necessary using pip on the folder where the binaries
are downloaded:

   pip install GDAL-3.3.1-cp38-cp38-win_amd64.whl

   pip install pyproj-3.1.0-cp39-cp38-win_amd64.whl

   pip install Fiona-1.8.20-cp38-cp38-win_amd64.whl

   pip install Shapely-1.7.1-cp38-cp38-win_amd64.whl

   pip install geopandas-0.9.0-py3-none-any.whl

Other required packages should also be installed
in the defined corresponding version in the following via pip:
osmnx==1.1.1, networkx>=2.5, numpy==1.20.3,
rasterio==1.2.4, affine==2.3.0, pandas==1.2.4

In order to run `examples <https://github.com/DLR-VF/PtAC-examples>`_,
jupyter notebook needs to be installed with the following command:

   pip install notebook

For further details see `python packaging instructions
<https://packaging.python.org/tutorials/installing-packages/>`_.


You can install PtAC with `pip <https://pypi.org/project/pip/>`_:

   pip install -i https://test.pypi.org/simple/ ptac

Usage
-----
To get started with PtAC, read the user reference and work through its
`examples <https://github.com/DLR-VF/PtAC-examples>`_.

Features
--------
PtAC is built on top of osmnx, geopandas, networkx and
uses `UrMoAC <https://github.com/DLR-VF/UrMoAC>`_ for accessibility computation.

* Download and prepare road networks from OpenStreetMap for accessibility calculation
* Calculate accessbilities from origins to the next destination
* Generate a population point dataset from population raster dataset
* Calculate Sustainable Development Goal 11.2 based on starting points with population information

.. toctree::
   :maxdepth: 2
   :caption: User Reference

   ptac

Support
--------

If you have a usage question please contact us via email (simon.nieland@dlr.de,
serra.yosmaoglu@dlr.de).

License
--------


Indices 
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
