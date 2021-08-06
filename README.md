# PtAC 0.0.1 alpha

PtAC is a Python package that allows users to automatically compute
public transport accessbilities for the Sustainable Development Goal
11.2. monitored by the proportion of the population that has convenient
access to public transport. Users can calculate accessibilities from
population points to public transit stops based on maximum distance or -
if defined - two different transit systems: low- and high-capacity.
Population points can be easily converted from rasters (.tif).

## Installation

You can install PtAC with [pip](https://pypi.org/project/pip/):

> pip install -i <https://test.pypi.org/simple/> ptac==0.0.1

In order to run examples, the user might need to install jupyterlab or
jupyter notebook with the following commands:

> pip install jupyterlab
>
> pip install notebook

See [python packaging
instructions](https://packaging.python.org/tutorials/installing-packages/)
for further details.

## Features

PtAC is built on top of osmnx, geopandas, networkx and uses UrMoAC
(<https://github.com/DLR-VF/UrMoAC>) for accessibility computation

-   Download and prepare road networks from OpenStreetMap for
    accessibility calculation
-   Calculate accessbilities from origins to the next destination
-   Generate a population point dataset from population raster dataset
-   Calculate Sustainable Development Goal 11.2 based on starting points
    with population information

::: {.toctree maxdepth="2" caption="User Reference"}
ptac
:::

## Support

If you have a usage question please contact us via email.

## License

The project is licensed under the MIT license.

# Indices

-   `genindex`{.interpreted-text role="ref"}
-   `modindex`{.interpreted-text role="ref"}
-   `search`{.interpreted-text role="ref"}
