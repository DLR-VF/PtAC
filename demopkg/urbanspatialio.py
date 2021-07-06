from geoalchemy2 import Geometry, WKTElement
import warnings
import pandas as pd
warnings.filterwarnings("ignore")


def to_postgis(geo_df, con, schema, table_name, if_exists="replace"):
    """

    :param geo_df:
    :param con:
    :param schema:
    :param table_name:
    :param if_exists:
    """
    # Fixed warning: UserWarning: Geometry column does not contain geometry.
    #gpd_copy = geo_df.copy()
    gpd_copy = pd.DataFrame(geo_df, copy=False)
    #gpd_copy['geometry'] = geo_df['geometry']
    gdf_srid = _extract_srid_int_from_crs(geo_df)
    gpd_copy.columns = gpd_copy.columns.str.replace(":", "_")
        #todo: decide what to do with nodes and members
    if "members" in gpd_copy.columns:
        del gpd_copy["members"]
    if "nodes" in gpd_copy.columns:
        del gpd_copy["nodes"]

    #gpd_copy=gpd_copy.replace({'{': ''}, regex=True)
    gpd_copy[geo_df.geometry.name] = gpd_copy.geometry.apply(lambda geom: WKTElement(geom.wkt, srid=gdf_srid))
    #if "index" in gpd_copy.columns:
    gpd_copy.to_sql(name=table_name, con=con, if_exists=if_exists,
                    schema=schema, dtype={geo_df.geometry.name: Geometry(geometry_type=_geom_type_to_postgis(geo_df),
                                                                            srid=gdf_srid)},  method='multi')



def from_postgis(db_name, host, user_name, password, schema_name, table_name):
    pass


def _geom_type_to_postgis(gdf):
    """
    Convert the geometry type of a GeoDataFrame to the PostGIS equivalent one.
    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
    Returns
    -------
    str:
    """
    if all(gdf.geom_type == 'Polygon'):
        postgis_geom_type = 'POLYGON'
    elif all(gdf.geom_type == 'MultiPolygon'):
        postgis_geom_type = 'MULTIPOLYGON'
    elif all(gdf.geom_type == 'Point'):
        postgis_geom_type = 'POINT'
    elif all(gdf.geom_type == 'LineString'):
        postgis_geom_type = 'LINESTRING'
    elif all(gdf.geom_type == 'MultiPoint'):
        postgis_geom_type = 'MULTIPOINT'
    elif all(gdf.geom_type == 'GeometryCollection'):
        postgis_geom_type = 'GEOMETRYCOLLECTION'
    elif all(gdf.geom_type == 'MultiLineString'):
        postgis_geom_type = 'MULTILINESTRING'
    else:
        postgis_geom_type = 'GEOMETRY'
    return postgis_geom_type


def _extract_srid_int_from_crs(geo_df):
    """
        Extracts EPSG Integer from GeoDataframe crs property dictionary

        Returns:
            EPSG integer
        """
        # old way of specifying crs = {'init': 'epsg:4326'}, prior to geopandas 0.7.0
    return int(geo_df.crs.srs.replace('epsg:', ''))

