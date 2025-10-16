#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Downloads pois, footprints and graphs from OSM"""
# ===========================================================================
__author__     = "Serra Yosmaoglu, Simon Nieland, Daniel Krajzewicz"
__copyright__  = "Copyright 2021-2025, German Aerospace Center (DLR), Institute of Transport Research"
__license__    = "EPL2.0"
__version__    = "0.2.0"
__maintainer__ = "Simon Nieland"
__email__      = "simon.nieland@dlr.de"
__status__     = "Production"
# ===========================================================================
# - https://github.com/DLR-VF/PtAC
# - http://www.dlr.de/vf
# ===========================================================================

# --- imports ---------------------------------------------------------------
import osmnx as ox


# --- functions -------------------------------------------------------------
def get_network(polygon, network_type="walk", custom_filter=None, simplify=False, verbose=0):
    """
    Download street network from osm via osmnx.

    :param polygon: boundary of the area from which to download the network (in WGS84)
    :type polygon: Geopandas.GeoDataFrame::POLYGON
    :param network_type: can be "all_private", "all", "bike", "drive", "drive_service",
        "walk" (see osmnx for description)
    :type network_type: str
    :param custom_filter: filter network (see osmnx for description)
    :type custom_filter: str
    :param verbose: Degree of verbosity (the higher, the more)
    :type verbose: int

    :return network_gdf: OSM city network
    :rtype network_gdf: GeoPandas.GeoDataFrame::LineString

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
            simplify=simplify,
        )
    )[1]
    return network_gdf
