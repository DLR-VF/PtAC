#!/usr/bin/env python3
# coding:utf-8
"""
@name : osm.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt
"""

import osmnx as ox


def get_facility(polygon, facility):
    return ox.pois_from_polygon(polygon, tags=facility)


def get_landuse(polygon, ):
    return ox.footprints_from_polygon(polygon, footprint_type="landuse")


def get_restaurants(polygon):
    return ox.pois_from_polygon(polygon, tags={"amenity": 'restaurant'})


def get_parks(polygon):
    return ox.pois_from_polygon(polygon, tags={"leisure": 'park'})


def get_network(polygon, network_type="walk", custom_filter=None, verbose=0):
    """
    Download street network from osm via osmnx

    :param polygon boundary of the area from which to download the network (in WGS84)
    :type polygon Geopandas.GeoDataFrame::POLYGON
    :param network_type can be ..
    :type network_type String
    :param custom_filter: filter network (see osmnx for description)
    :type custom_filter: String
    :param verbose: Degree of verbosity (the higher, the more)
    :type verbose: Integer
    :return Network graph
    :rtype networkx.Graph
    """
    if verbose > 0:
        print("downloading street network. This may take some time for bigger areas\n")
    bounds = polygon.unary_union.bounds
    return ox.graph_to_gdfs(ox.graph_from_bbox(north=bounds[3], south=bounds[1], east=bounds[2], west=bounds[0],
                                               custom_filter=custom_filter,
                                               network_type=network_type,
                                               simplify=False))[1]


def get_buildings(polygon):
    return ox.footprints.footprints_from_polygon(polygon, footprint_type='building', retain_invalid=False)
