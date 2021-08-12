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


## Install and Usage

Please see the [user guide](docs/source/README.rst) for information about installation and usage.

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
