#!/usr/bin/env python3
# coding:utf-8

import osmnx as ox

"""Downloads pois, footprints and graphs from OSM"""

"""
@name : osm.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt
"""


def get_network(polygon, network_type="walk", custom_filter=None, verbose=0):
    """
    Download street network from osm via osmnx.

    :param polygon: boundary of the area from which to download the network (in WGS84)
    :type polygon: Geopandas.GeoDataFrame::POLYGON
    :param network_type: can be "all_private", "all", "bike", "drive", "drive_service", "walk" (see osmnx for description)
    :type network_type: str
    :param custom_filter: filter network (see osmnx for description)
    :type custom_filter: str
    :param verbose: Degree of verbosity (the higher, the more)
    :type verbose: int
    :return OSM city network
    :rtype GeoDataFrame::LineString

    """
    if verbose > 0:
        print("downloading street network. This may take some time for bigger areas\n")
    bounds = polygon.unary_union.bounds
    network_gdf = ox.graph_to_gdfs(
        ox.graph_from_bbox(
            north=bounds[3],
            south=bounds[1],
            east=bounds[2],
            west=bounds[0],
            custom_filter=custom_filter,
            network_type=network_type,
            simplify=False,
        )
    )[1]
    return network_gdf
