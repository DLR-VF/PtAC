<!-- PtAC documentation master file, created by
sphinx-quickstart on Fri Jul  9 10:40:37 2021.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# PtAC 0.0.3 alpha

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
[OpenStreetMaps (OSM)](https://wiki.openstreetmap.org/wiki/Public_transport) or
[General Transit Feed Specification (GTFS)](https://gtfs.org/) feeds.
If not available, the city network dataset is prepared within the module accessibility
and downloaded as csv.

# Installation

You can install PtAC with [pip](https://pypi.org/project/pip/):

> pip install -i [https://test.pypi.org/simple/](https://test.pypi.org/simple/) ptac

There are certain packages are required to be installed before using the package.

Windows users should download the following binaries on a specific folder
from [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/):
GDAL, Pyproj (v3.1.0), Fiona, Shapely (v1.7.1) and Geopandas (v0.9.0)
in the correct version of Python
and operating system (32-bit or 64-bit) is installed on the computer
(e.g. for Python version 3.9x (64-bit), GDAL-3.3.1-cp39-cp39-win_amd64.whl should be installed).
The following order of installation is necessary using pip on the folder where the binaries
are downloaded:

> pip install GDAL-3.3.1-cp39-cp39-win_amd64.whl

> pip install pyproj-3.1.0-cp39-cp39-win_amd64.whl

> pip install Fiona-1.8.20-cp39-cp39-win_amd64.whl

> pip install Shapely-1.7.1-cp39-cp39-win_amd64.whl

> pip install geopandas-0.9.0-py3-none-any.whl

Other required packages should also be installed
in the defined corresponding version in the following via pip:
osmnx==1.1.1, networkx>=2.5, numpy==1.20.3,
rasterio==1.2.4, affine==2.3.0, pandas==1.2.4

In order to demonstrate [examples](https://github.com/DLR-VF/PtAC-examples),
jupyter notebook needs to be installed with the following command:

> pip install notebook

For further details see [python packaging instructions](https://packaging.python.org/tutorials/installing-packages/).

# Usage

To get started with PtAC, read the user reference and see sample code and input data in
[examples repository](https://github.com/DLR-VF/PtAC-examples).

# Features

PtAC is built on top of osmnx, geopandas, networkx and
uses [UrMoAC](https://github.com/DLR-VF/UrMoAC) for accessibility computation.


* Download and prepare road networks from OpenStreetMap for accessibility calculation


* Calculate accessbilities from origins to the next destination


* Generate a population point dataset from population raster dataset


* Calculate Sustainable Development Goal 11.2 based on starting points with population information

# Support

If you have a usage question please contact us via email ([simon.nieland@dlr.de](mailto:simon.nieland@dlr.de),
[serra.yosmaoglu@dlr.de](mailto:serra.yosmaoglu@dlr.de)).
