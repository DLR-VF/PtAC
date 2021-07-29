<!-- PtAC documentation master file, created by
sphinx-quickstart on Fri Jul  9 10:40:37 2021.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# PtAC 0.0.1 alpha

PtAC is a Python package that allows users to automatically compute public transport
accessbilities for the Sustainable Development Goal 11.2. monitored by the proportion
of the population that has convenient access to public transport.
Users can calculate accessibilities from population points to public transit stops
based on maximum distance or - if defined - two different transit systems:
low- and high-capacity.
Population points can be easily converted from rasters (.tif).

## Installation

Installation instructions will be shown here:
You can install PtAC with pip:

> pip install ptac

## Features

PtAC is built on top of osmnx, geopandas, networkx and
uses UrMoAC ([https://github.com/DLR-VF/UrMoAC](https://github.com/DLR-VF/UrMoAC)) for accessibility computation


* Download and prepare road networks from OpenStreetMap for accessibility calculation


* Calculate accessbilities from origins to the next destination


* Generate a population point dataset from population raster dataset


* Calculate Sustainable Development Goal 11.2 based on starting points with population information

## User Reference


* PtAC.accessibility module


* PtAC.osm module


## Support

## License

The project is licensed under the (XXXMITXXX) license.

# Indices


* Index


* Module Index


* Search Page