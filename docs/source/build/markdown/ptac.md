User reference for the PtAC package.

This guide covers usage of all public modules and functions.
Every function can be accessed via ptac.module_name.function_name().

# ptac.accessibility module

@name : accessibility.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021 12:44
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt


### ptac.accessibility.build_request(epsg, number_of_threads, date, start_time)
Builds requests for the UrMoAC


* **Parameters**

    
    * **epsg** (*String*) – PSG code of UTM projection for a certain area of interest


    * **number_of_threads** (*String*) – PSG code of UTM projection for a certain area of interest


    * **date** (*integer*) – date on which the routing starts (e.g. 20200915)


    * **start_time** (*Integer*) – time to start the routing (in seconds of the day)



### ptac.accessibility.calculate_sdg(df_pop_total, pop_accessible, population_column, verbose=0)

* **Parameters**

    
    * **df_pop_total** – 


    * **pop_accessible** – 


    * **population_column** – 



* **Returns**

    


* **Return type**

    


### ptac.accessibility.distance_to_closest(start_geometries, destination_geometries, network_gdf=None, boundary_geometries=None, transport_system=None, maximum_distance=None, start_time=35580, number_of_threads=1, date=20200915, verbose=0)
Python wrapper for UrMoAC Accessibility Calculator


* **Parameters**

    
    * **network_gdf** (*Geopandas.GeoDataFrame::POLYGON*) – network dataset to use (optional, if None is provided dataset will be downloaded from osm automatically)


    * **start_geometries** (*Geopandas.GeoDataFrame::POLYGON*) – Starting points for accessibility calculation


    * **destination_geometries** (*Geopandas.GeoDataFrame::POLYGON*) – Starting point for accessibility calculation


    * **boundary_geometries** (*Geopandas.GeoDataFrame::POLYGON*) – 


    * **maximum_distance** – Maximum distance to next pt station (optional)


rtype maximum_distance: Integer
:param start_time: time to start the routing (in seconds of the day)
:type start_time: Integer
:param transport_system:
:type transport_system:
:param number_of_threads:
:type number_of_threads: Integer
:param date:
:type date:
:param verbose: The degree of verbosity. Valid values are 0 (silent) - 3 (debug)
:type verbose:


### ptac.accessibility.prepare_network(network_gdf=None, boundary=None, verbose=0)
Loads road network from OpenStreetMap and prepares network for usage in UrMoAC


* **Parameters**

    
    * **network_gdf** – network dataset to use (optional, if None is provided dataset will be downloaded from osm automatically)


    * **boundary** (*Geopandas.GeoDataFrame:POLYGON*) – boundary of area where to download network (must be projected in WGS84)


    * **epsg** (*Integer*) – EPSG code of UTM projection for the area of interest


    * **verbose** (*Integer*) – The degree of verbosity. Valid values are 0 (silent) - 3 (debug)



### ptac.accessibility.prepare_origins_and_destinations(dest_gdf, od='origin')
prepares origin or desination data set for usage in UrMoAC


* **Parameters**

    
    * **dest_gdf** (*Geopandas.GeoDataFrame:POINT*) – origin or destination point data set (must be projected in UTM Projection)


    * **od** (*String*) – indicate if “origin” or “destination”



### ptac.accessibility.subset_result(accessibility_output, transport_system=None, maximum_distance=None)

* **Parameters**

    
    * **accessibility_output** – 


    * **transport_system** – 


    * **maximum_distance** – 



* **Returns**

    


* **Return type**

    

# ptac.osm module

@name : osm.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt


### ptac.osm.get_network(polygon, network_type='walk', custom_filter=None, verbose=0)
Download street network from osm via osmnx


* **Parameters**

    
    * **polygon** (*Geopandas.GeoDataFrame::POLYGON*) – boundary of the area from which to download the network (in WGS84)


    * **network_type** (*String*) – can be ..


    * **custom_filter** (*String*) – filter network (see osmnx for description)


    * **verbose** (*Integer*) – Degree of verbosity (the higher, the more)


:return Network graph
:rtype networkx.Graph

# ptac.population module

@name : population.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt


### ptac.population.raster_to_points(path, band=1, epsg=4326)

* **Parameters**

    
    * **path** (*String*) – path to raster file. (Tested with GeoTIF)


    * **band** (*int*) – Band of dataset



* **Returns**

    Point GeoDataFrame including Raster values of specific band



* **Return type**

    GeoPandas.GeoDataFrame:: Point


# ptac.util module

@name : util.py
Copyright (c) 2016–2021 Geoff Boeing [https://geoffboeing.com/](https://geoffboeing.com/)


### ptac.util.project_gdf(gdf, geom_col='geometry', to_crs=None, to_latlong=False)
Project a GeoDataFrame to the UTM zone appropriate for its geometries’
centroid.

The simple calculation in this function works well for most latitudes, but
won’t work for some far northern locations like Svalbard and parts of far
northern Norway.


* **Parameters**

    
    * **gdf** (*GeoDataFrame*) – the gdf to be projected


    * **to_crs** (*dict*) – if not None, just project to this CRS instead of to UTM


    * **to_latlong** (*bool*) – if True, projects to latlong instead of to UTM



* **Returns**

    


* **Return type**

    GeoDataFrame



### ptac.util.project_geometry(geometry, crs=None, to_crs=None, to_latlong=False)
Project a shapely Polygon or MultiPolygon from lat-long to UTM, or
vice-versa


* **Parameters**

    
    * **geometry** (*shapely Polygon or MultiPolygon*) – the geometry to project


    * **crs** (*dict*) – the starting coordinate reference system of the passed-in geometry,
    default value (None) will set settings.default_crs as the CRS


    * **to_crs** (*dict*) – if not None, just project to this CRS instead of to UTM


    * **to_latlong** (*bool*) – if True, project from crs to lat-long, if False, project from crs to
    local UTM zone



* **Returns**

    (geometry_proj, crs), the projected shapely geometry and the crs of the
    projected geometry



* **Return type**

    tuple
