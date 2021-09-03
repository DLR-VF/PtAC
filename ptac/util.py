#!/usr/bin/env python3
# coding:utf-8

"""Converts geometries between latitude/longitude & UTM coordinates"""

"""
@name : util.py
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt & 2016–2021 Geoff Boeing https://geoffboeing.com/
"""

#from osmnx
import geopandas as gpd
import math
import ptac.settings as settings
from shapely.geometry import Polygon
import pandas as pd
from pyproj import CRS


# from osmnx
def project_geometry(geometry, crs=None, to_crs=None, to_latlong=False):
    """
        Project a shapely Polygon or MultiPolygon from lat-long to UTM, or vice-versa

        :param geometry: shapely Polygon or MultiPolygon the geometry to project
        :type geometry: Geopandas.GeoDataFrame::POLYGON
        :param crs: The starting coordinate reference system of the passed-in geometry,
        default value (None) will set settings.default_crs as the CRS
        :type crs: dict
        :param to_crs: if not None, just project to this CRS instead of to UTM
        :type to_crs: dict
        :param to_latlong: if True, project from crs to lat-long, if False, project from crs to
        local UTM zone
        :type to_latlong: bool
        :return: (geometry_proj, crs), the projected shapely geometry and the crs of the
        projected geometry
        :rtype: tuple
    """

    if crs is None:
        crs = settings.default_crs

    gdf = gpd.GeoDataFrame()
    gdf.crs = crs
    gdf.gdf_name = 'geometry to project'
    gdf['geometry'] = None
    gdf.loc[0, 'geometry'] = geometry
    gdf_proj = project_gdf(gdf, to_crs=to_crs, to_latlong=to_latlong)
    geometry_proj = gdf_proj['geometry'].iloc[0]
    return geometry_proj, gdf_proj.crs


def project_gdf(gdf, geom_col="geometry", to_crs=None, to_latlong=False):
    """
        Project a GeoDataFrame to the UTM zone appropriate for its geometries'
        centroid.
    
        The simple calculation in this function works well for most latitudes, but
        won't work for some far northern locations like Svalbard and parts of far
        northern Norway.

        :param gdf: the gdf to be projected
        :type gdf: Geopandas.GeoDataFrame::POINT
        :param to_crs: CRS code. if not None, just project to this CRS instead of to UTM
        :type to_crs: int
        :param to_latlong : If True, projects to latlong instead of to UTM
        :type to_latlong: bool
        :return projected_gdf: A projected GeoDataFrame to the UTM zone
        :rtype projected_gdf: Geopandas.GeoDataFrame::POINT
    """
    assert len(gdf) > 0, 'You cannot project an empty GeoDataFrame.'

    # if gdf has no gdf_name attribute, create one now
    if not hasattr(gdf, 'gdf_name'):
        gdf.gdf_name = 'unnamed'

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
            if (gdf.crs is not None) and gdf.crs.is_geographic==False:
                return gdf

            # calculate the centroid of the union of all the geometries in the
            # GeoDataFrame
            avg_longitude = gdf[geom_col].unary_union.centroid.x

            # calculate the UTM zone from this avg longitude and define the UTM
            # CRS to project
            utm_zone = int(math.floor((avg_longitude + 180) / 6.) + 1)
            utm_crs = f"+proj = utm + datum = WGS84 + ellps = WGS84 + zone = {utm_zone} + units = m + type = crs"
            crs = CRS.from_proj4(utm_crs)
            epsg = crs.to_epsg()
            projected_gdf = gdf.to_crs(epsg)

    projected_gdf.gdf_name = gdf.gdf_name
    return projected_gdf
