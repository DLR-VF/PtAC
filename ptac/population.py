#!/usr/bin/env python3
# coding:utf-8

"""Converts population raster dataset to population points"""

"""
@name : population.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from affine import Affine


def raster_to_points(path, band=1, epsg=4326):
    """
    :param path: path to raster file. (Tested with GeoTIF)
    :type path: String
    :param band: Band of dataset
    :type band: int
    :return: Point GeoDataFrame including Raster values of specific band
    :rtype: GeoPandas.GeoDataFrame:: Point
    """

    with rasterio.open(path) as ds:
        arr = ds.read(band)
        t0 = ds.transform

    t1 = t0 * Affine.translation(0.5, 0.5)

    # Needed to move Affine object to left side to get rid of
    # DeprecationWarning: Right multiplication will be prohibited in version 3.0
    rc2xy = lambda r, c: t1 * (c, r)

    x_coordinates = []
    y_coordinates = []
    values = []

    for x in range(0, arr.shape[0]):
        for y in range(0, arr.shape[1]):
            if not np.isnan(arr[x, y]) and arr[x, y] != 0.0:
                values.append(arr[x, y])
                x_coordinates.append(rc2xy(x, y)[0])
                y_coordinates.append(rc2xy(x, y)[1])

    df = pd.DataFrame({
        "pop": values,
        "x_coord": x_coordinates,
        "y_coord": y_coordinates})
    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x_coord, df.y_coord), crs=f"EPSG:{epsg}")

    return geo_df


def download_population_raster(bounds, request):
    print()



def save_to_disk(input_path, output_path, driver='ESRI Shapefile'):

    cities = os.listdir(rf'{input_path}')
    for city in cities:
        if city.endswith("tif"):
            print(f"processing {city}")
            raster_path = rf'{input_path}/{city}'
            if driver == "GPKG":
                points_gdf = raster_to_points(raster_path, band=1, epsg=4326)
                city_name = city.split(".")[0].lower()
                points_gdf.to_file(f"{output_path}/{city_name}_pop_point.gpkg", driver="GPKG")
                print(f"{city} population points saved as gpkg file")
            elif driver == 'ESRI Shapefile':
                points_gdf = raster_to_points(raster_path, band=1, epsg=4326)
                city_name = city.split(".")[0].lower()
                points_gdf.to_file(f"{output_path}/{city_name}_pop_point.{driver}", driver="ESRI Shapefile")
                print(f"{city} population points saved as {driver} file")
            elif driver == "CSV":
                points_gdf = raster_to_points(raster_path, band=1, epsg=4326)
                city_name = city.split(".")[0].lower()
                points_gdf.to_csv(f"{output_path}/{city_name}_pop_point.{driver}", sep=";", header=False)
                print(f"{city} population points saved as {driver} file")
            else:
                print(f"{driver} extension is not supported")
