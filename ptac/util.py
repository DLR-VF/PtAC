#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Converts geometries between latitude/longitude & UTM coordinates

Uses methods developed by Geoff Boeing https://geoffboeing.com/
"""
# ===========================================================================
__author__ = "Serra Yosmaoglu, Simon Nieland, Daniel Krajzewicz"
__copyright__ = "Copyright 2021-2025, German Aerospace Center (DLR), Institute of Transport Research"
__license__ = "EPL2.0"
__version__ = "0.2.0"
__maintainer__ = "Simon Nieland"
__email__ = "simon.nieland@dlr.de"
__status__ = "Production"
# ===========================================================================
# - https://github.com/DLR-VF/PtAC
# - http://www.dlr.de/vf
# ===========================================================================

# --- imports ---------------------------------------------------------------
import math

from pyproj import CRS

import ptac.settings as settings


# --- functions -------------------------------------------------------------
# from osmnx
def project_gdf(gdf, geom_col="geometry", to_crs=None, to_latlong=False):
    """
    Project a GeoDataFrame to the UTM zone appropriate for its geometries' centroid.

    The simple calculation in this function works well for most latitudes, but
    won't work for some far northern locations like Svalbard and parts of far
    northern Norway.

    :param gdf: the gdf to be projected
    :type gdf: Geopandas.GeoDataFrame::POINT
    :param to_crs: CRS code. if not None,project GeodataFrame to CRS
    :type to_crs: int
    :param to_latlong: If True, projects to latlong instead of to UTM
    :type to_latlong: bool
    :return projected_gdf: A projected GeoDataFrame
    :rtype projected_gdf: Geopandas.GeoDataFrame::POINT
    """
    assert len(gdf) > 0, "You cannot project an empty GeoDataFrame."

    # if gdf has no gdf_name attribute, create one now
    if not hasattr(gdf, "gdf_name"):
        gdf.gdf_name = "unnamed"

    # if to_crs was passed-in, use this value to project the gdf
    if to_crs is not None:
        projected_gdf = gdf.to_crs(to_crs)

    # if to_crs was not passed-in, calculate the centroid of the geometry to
    # determine UTM zone
    else:
        if to_latlong:
            # if to_latlong is True, project the gdf to latlong
            latlong_crs = settings.default_crs
            projected_gdf = gdf.to_crs(latlong_crs)

        else:
            # else, project the gdf to UTM
            # if GeoDataFrame is already in UTM, just return it
            if (gdf.crs is not None) and (gdf.crs.is_geographic is False):
                return gdf

            # calculate the centroid of the union of all the geometries in the
            # GeoDataFrame
            avg_longitude = gdf[geom_col].union_all().centroid.x

            # calculate the UTM zone from this avg longitude and define the UTM
            # CRS to project
            utm_zone = int(math.floor((avg_longitude + 180) / 6.0))
            utm_crs = f"+proj = utm + datum = WGS84 + ellps = WGS84 + zone = {utm_zone} + units = m + type = crs"
            crs = CRS.from_proj4(utm_crs)
            epsg = crs.to_epsg()
            projected_gdf = gdf.to_crs(epsg)

    projected_gdf.gdf_name = gdf.gdf_name
    return projected_gdf
