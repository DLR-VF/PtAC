#!/usr/bin/env python3
# coding:utf-8

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio


"""Converts population raster dataset to population points"""

"""
@name : population.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung,
Deutsches Zentrum fuer Luft- und Raumfahrt
"""


def raster_to_points(path, band=1, epsg=4326):
    """
        :param path: Path to raster file. (Tested with GeoTIF)
        :type path: str
        :param band: Band of dataset
        :type band: int
        :return: Point GeoDataFrame including Raster values of specific band
        :rtype: GeoPandas.GeoDataFrame:: Point
    """

    with rasterio.open(path) as src:
        # create 1D coordinate arrays (coordinates of the pixel center)
        xmin, ymax = np.around(src.xy(0.00, 0.00), 9)  # src.xy(0, 0)
        xmax, ymin = np.around(src.xy(src.height-1, src.width-1), 9)  # src.xy(src.width-1, src.height-1)
        x = np.linspace(xmin, xmax, src.width)
        y = np.linspace(ymax, ymin, src.height)  # max -> min so coords are top -> bottom

        # create 2D arrays
        xs, ys = np.meshgrid(x, y)
        pop = src.read(1)

        # Apply NoData mask
        mask = src.read_masks(1) > 0
        xs, ys, pop = xs[mask], ys[mask], pop[mask]

    data = {"X": pd.Series(xs.ravel()), "Y": pd.Series(ys.ravel()), "pop": pd.Series(pop.ravel())}
    df = pd.DataFrame(data=data)
    df = df[df['pop'] > 0]
    geometry = gpd.points_from_xy(df.X, df.Y)
    geo_df = gpd.GeoDataFrame(df, crs=f"EPSG:{epsg}", geometry=geometry)
    return geo_df
