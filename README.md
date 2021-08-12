<!-- PtAC documentation master file, created by
sphinx-quickstart on Fri Jul  9 10:40:37 2021.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# PtAC 0.0.3 alpha

PtAC is a Python package to automatically compute walking
accessibilities from residential areas to public transport stops for the Sustainable Development Goal 11.2
defined by the United Nations. The goal aims to measure and monitor the proportion
of the population in a city that has convenient access to public transport
(see https://sdgs.un.org/goals/goal11). With this library users can download and process [OpenStreetMap](https://www.openstreetmap.org) (OSM)
street networks and population information worldwide. Based on this it is possible to calculate accessibilities
from population points to public transit stops based on minimum street network distance.

In order to calculate SDG 11.2.1 indicator the necessary input sources are
population information, public transit stops and city networks.
Worldwide population information can be downloaded via WMS 
from [World Settlement Footprint](https://figshare.com/articles/dataset/World_Settlement_Footprint_WSF_2015/10048412)
(WSF) and converted
to points. Public transit stops can be obtained from
[OpenStreetMap (OSM)](https://wiki.openstreetmap.org/wiki/Public_transport) or
[General Transit Feed Specification (GTFS)](https://gtfs.org/) feeds (have a look at the examples if you want to know how this
works exactly). The street network can be downloaded and prepared for routing automatically within the library.


## Install and Usage

Please see the [user guide](docs/source/user-guide.rst) for information about installation and usage.

# Examples

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
