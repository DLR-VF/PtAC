#from osmnx
import geopandas as gpd
import math
import ptac.settings as settings
from shapely.geometry import Polygon
import pandas as pd

#from https://github.com/mthh/gpd_lite_toolbox/blob/ce4553c139775953c49d8756960d0a166b67c6bf/gpd_lite_toolbox/core.py#L565
def make_grid(gdf, height, cut=True):
    """
    Return a grid, based on the shape of *gdf* and on a *height* value (in
    units of *gdf*). If cut=False, the grid will not be intersected with *gdf*
    (i.e it makes a grid on the bounding-box of *gdf*).
    Parameters
    ----------
    gdf: GeoDataFrame
        The collection of polygons to be covered by the grid.
    height: Integer
        The dimension (will be used as height and width) of the ceils to create,
        in units of *gdf*.
    cut: Boolean, default True
        Cut the grid to fit the shape of *gdf* (ceil partially covering it will
        be truncated). If False, the returned grid will fit the bounding box
        of *gdf*.
    Returns
    -------
    grid: GeoDataFrame
        A collection of polygons.
    """
    from math import ceil
    from shapely.ops import unary_union
    xmin, ymin = [i.min() for i in gdf.bounds.T.values[:2]]
    xmax, ymax = [i.max() for i in gdf.bounds.T.values[2:]]
    rows = int(ceil((ymax-ymin) / height))
    cols = int(ceil((xmax-xmin) / height))

    x_left_origin = xmin
    x_right_origin = xmin + height
    y_top_origin = ymax
    y_bottom_origin = ymax - height

    res_geoms = []
    for countcols in range(cols):
        y_top = y_top_origin
        y_bottom = y_bottom_origin
        for countrows in range(rows):
            res_geoms.append((
                (x_left_origin, y_top), (x_right_origin, y_top),
                (x_right_origin, y_bottom), (x_left_origin, y_bottom)
                ))
            y_top = y_top - height
            y_bottom = y_bottom - height
        x_left_origin = x_left_origin + height
        x_right_origin = x_right_origin + height
    if cut:
        if all(gdf.eval(
            "geometry.type =='Polygon' or geometry.type =='MultiPolygon'")):
            res = gpd.GeoDataFrame(
                geometry=pd.Series(res_geoms).apply(lambda x: Polygon(x)),
                crs=gdf.crs
                ).intersection(unary_union(gdf.geometry))
        else:
            res = gpd.GeoDataFrame(
                geometry=pd.Series(res_geoms).apply(lambda x: Polygon(x)),
                crs=gdf.crs
                ).intersection(unary_union(gdf.geometry).convex_hull)
        res = res[res.geometry.type == 'Polygon']
        res.index = [i for i in range(len(res))]
        grid = gpd.GeoDataFrame(geometry=res)
        grid = grid[~grid.is_empty]
        return grid

    else:
        return gpd.GeoDataFrame(
            index=[i for i in range(len(res_geoms))],
            geometry=pd.Series(res_geoms).apply(lambda x: Polygon(x)),
            crs=gdf.crs
            )


# from osmnx
def project_geometry(geometry, crs=None, to_crs=None, to_latlong=False):
    """
    Project a shapely Polygon or MultiPolygon from lat-long to UTM, or
    vice-versa

    Parameters
    ----------
    geometry : shapely Polygon or MultiPolygon
        the geometry to project
    crs : dict
        the starting coordinate reference system of the passed-in geometry,
        default value (None) will set settings.default_crs as the CRS
    to_crs : dict
        if not None, just project to this CRS instead of to UTM
    to_latlong : bool
        if True, project from crs to lat-long, if False, project from crs to
        local UTM zone

    Returns
    -------
    tuple
        (geometry_proj, crs), the projected shapely geometry and the crs of the
        projected geometry
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

    Parameters
    ----------
    gdf : GeoDataFrame
        the gdf to be projected
    to_crs : dict
        if not None, just project to this CRS instead of to UTM
    to_latlong : bool
        if True, projects to latlong instead of to UTM

    Returns
    -------
    GeoDataFrame
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
            projected_gdf = gdf[geom_col].to_crs(latlong_crs)

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
            utm_crs = {'datum': 'WGS84',
                       'ellps': 'WGS84',
                       'proj': 'utm',
                       'zone': utm_zone,
                       'units': 'm'}

            # project the GeoDataFrame to the UTM CRS
            projected_gdf = gdf.to_crs(utm_crs)

    projected_gdf.gdf_name = gdf.gdf_name
    return projected_gdf