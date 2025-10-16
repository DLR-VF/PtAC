# PtAC

PtAC is a Python package to automatically compute walking accessibilities from residential areas to public transport stops for the Sustainable Development Goal 11.2 defined by the United Nations.
The goal is to measure and monitor the proportion of the population in a city that has convenient access to public transport (see https://sdgs.un.org/goals/goal11).
With this library users can download and process [OpenStreetMap](https://www.openstreetmap.org) (OSM) street networks and population information worldwide.
Based on this it is possible to calculate accessibilities from population points to public transit stops based on minimum street network distance.

For calculating the SDG 11.2.1 indicator information about the population, public transit stops and city networks is needed.
Worldwide population information can be downloaded via WMS from [World Settlement Footprint](https://www.nature.com/articles/s41597-020-00580-5)
(WSF) and converted to points.
Public transit stops can be obtained from [OpenStreetMap (OSM)](https://wiki.openstreetmap.org/wiki/Public_transport) or [General Transit Feed Specification (GTFS)](https://gtfs.org/) feeds (have a look at the examples if you want to know how this works exactly).
The street network can be downloaded and prepared for routing automatically within the library.

When using it, please cite:

* Nieland, S., Goletz, M., Krajzewicz, D. & Palacios Lopez, D. (2025) <a href="https://elib.dlr.de/215357/">Introducing PtAC – an open source tool to assess SDG 11.2 using open data</a>. Transportation Research Interdisciplinary Perspectives (32). Elsevier. doi: 10.1016/j.trip.2025.101516. ISSN 2590-1982. 



# Installation and Usage

Please see the [user guide](https://github.com/DLR-VF/PtAC/blob/master/docs/source/index.rst) for information about installation and usage.

# Examples

To get started with PtAC, read the user reference and see sample code and input data in [examples repository](https://github.com/DLR-VF/PtAC-examples).

# Features

PtAC is built on top of osmnx, geopandas, networkx and uses [UrMoAC](https://github.com/DLR-VF/UrMoAC) for accessibility computation.

* Download and prepare road networks from OpenStreetMap for accessibility calculation
* Generate a population point dataset from population raster dataset
* Calculate accessibilities from origins to the next destination
* Calculate Sustainable Development Goal 11.2 based on starting points with population information
  
# Authors

* [Simon Nieland](https://github.com/SimonNieland) 
* [Serra Yosmaoglu](https://github.com/serrayos)
* [Daniel Krajzewicz](https://github.com/dkrajzew) 

# Contributors

* Mirko Goletz
* [Andreas Radke](https://github.com/orgs/DLR-VF/people/schakalakka) 

# Support

If you have a usage question, please contact us via email ([simon.nieland@dlr.de](mailto:simon.nieland@dlr.de), [Daniel.Krajzewicz@dlr.de](mailto:daniel.krajzewicz@dlr.de)).

# License Information  

PtAC is licensed under the Eclipse Public License 2.0. See the [LICENSE.md](https://github.com/DLR-VF/PtAC/blob/master/LICENSE.md) file for more information.

# Disclaimer

* We have chosen some links to external pages as we think they contain useful information. However, we are not responsible for the contents of the pages we link to.
* The software is provided "AS IS".
* We tested the software, and it worked as expected. Nonetheless, we cannot guarantee it will work as you expect.

# References

* Nieland, S., Goletz, M., Krajzewicz, D. & Palacios Lopez, D. (2025) <a href="https://elib.dlr.de/215357/">Introducing PtAC – an open source tool to assess SDG 11.2 using open data</a>. Transportation Research Interdisciplinary Perspectives (32). Elsevier. doi: 10.1016/j.trip.2025.101516. ISSN 2590-1982. 

* Boeing, G. (2017). OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks. 
  Computers, Environment and Urban Systems 65, 126-139. doi:10.1016/j.compenvurbsys.2017.05.004

* Krajzewicz, D., Heinrichs, D. & Cyganski, R. (2017). Intermodal Contour Accessibility Measures Computation Using the 'UrMo Accessibility Computer'. 
  International Journal On Advances in Systems and Measurements, 10 (3&4), Seiten 111-123. IARIA.

* Palacios-Lopez, D., Bachofer, F., Esch, T., Heldens, W., Hirner, A., Marconcini, M., ... & Reinartz, P. (2019). 
  New perspectives for mapping global population distribution using world settlement footprint products. Sustainability, 11(21), 6056.

* Palacios-Lopez, D., Bachofer, F., Esch, T., Marconcini, M., MacManus, K., Sorichetta, A., ... & Reinartz, P. (2021). 
  High-Resolution Gridded Population Datasets: Exploring the Capabilities of the World Settlement Footprint 2019 
  Imperviousness Layer for the African Continent. Remote Sensing, 13(6), 1142.

* Marconcini, M., Metz-Marconcini, A., Üreyen, S., Palacios-Lopez, D., Hanke, W., Bachofer, F., ... & Strano, E. (2020). 
  Outlining where humans live, the World Settlement Footprint 2015. Scientific Data, 7(1), 1-14.
