#!/usr/bin/env python3
# coding:utf-8

import glob
import os
import sys
import time
import timeit
from pathlib import Path

import geopandas as gpd
import pandas as pd

import ptac.osm as osm
import ptac.settings as settings
import ptac.util as util

"""Prepares dataset for accessibility computation and computes walking accessibilities
   from residential areas to public transport stops."""

"""
@name : accessibility.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021 12:44
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt
"""

# global home_directory
home_directory = Path.home()  # os.path.abspath('../../')  # Path.home()


def clear_directory(folder=f"{home_directory}/.ptac"):
    files = glob.glob(f"{folder}//*.csv")
    for f in files:
        try:
            os.remove(f)
        except os.error as e:
            print("Error: %s : %s" % (f, e.strerror))


def prepare_origins_and_destinations(dest_gdf, od):
    """
    Prepare origin or destination dataset for usage in UrMoAC.

    :param dest_gdf: origin or destination point data set (must be projected in UTM Projection)
    :type dest_gdf: Geopandas.GeoDataFrame:POINT
    :param od: indicate if "origin" or "destination"
    :rtype od: str
    """
    dest_gdf["x"] = dest_gdf.geometry.centroid.x
    dest_gdf["y"] = dest_gdf.geometry.centroid.y
    dest_gdf = dest_gdf[["x", "y"]]
    if od == "origin":
        dest_gdf = dest_gdf.dropna()
        dest_gdf.to_csv(f"{home_directory}/.ptac/origins.csv", sep=";", header=False)
    if od == "destination":
        dest_gdf = dest_gdf.dropna()
        dest_gdf.to_csv(
            f"{home_directory}/.ptac/destinations.csv", sep=";", header=False
        )


def prepare_network(network_gdf=None, boundary=None, verbose=0):
    """
    Load road network from OpenStreetMap and prepares network for usage in UrMoAC.

    :param network_gdf: network dataset to use
           (optional, if None is provided dataset will be downloaded from osm automatically)
    :param boundary: boundary of area where to download network (must be projected in WGS84)
    :type boundary: Geopandas.GeoDataFrame:POLYGON
    :param epsg: EPSG code of UTM projection for the area of interest
    :type epsg: int
    :param verbose: The degree of verbosity. Valid values are 0 (silent) - 3 (debug)
    :rtype verbose: int

    """
    if network_gdf is None:
        if verbose > 0:
            print("No street network was specified. Loading osm network..\n")
        network_gdf = osm.get_network(boundary)
        network_gdf = util.project_gdf(network_gdf, to_latlong=True)
        # network_gdf = util.project_gdf(network_gdf, to_latlong=False)

    else:
        if verbose > 0:
            print("Street network provided\n")
        # todo: check if dataset has the right format

    if verbose > 0:
        print("Preparing street network for routing")

    network_characteristics = settings.streettypes
    if "street_type" not in network_characteristics.columns:
        network_characteristics.reset_index(inplace=True)
        network_characteristics.rename(columns={"index": "street_type"}, inplace=True)
    network_gdf.reset_index(inplace=True)
    network_gdf = network_gdf.rename(
        columns={
            "u": "fromnode",
            "v": "tonode",
            "maxspeed": "vmax_osm",
            "highway": "street_type",
            "lanes": "lanes_osm",
            "index": "oid",
        }
    )
    network_gdf = network_gdf.merge(
        network_characteristics, on="street_type", how="left"
    )
    network_gdf = network_gdf.reset_index()
    network_gdf = network_gdf[
        [
            "index",
            "fromnode",
            "tonode",
            "mode_walk",
            "mode_bike",
            "mode_mit",
            "vmax",
            "length",
            "geometry",
        ]
    ]
    network_gdf = pd.concat([network_gdf, network_gdf.geometry.bounds], axis=1)
    del network_gdf["geometry"]
    network_gdf.to_csv(
        f"{home_directory}/.ptac/network.csv", sep=";", header=False, index=False
    )
    return network_gdf


def build_request(epsg, number_of_threads, date, start_time, timestamp):
    """
    Build request for the UrMoAC.

    :param epsg: PSG code of UTM projection for a certain area of interest
    :type epsg: str
    :param number_of_threads: The number of threads to use
    :type number_of_threads: int
    :param date: Date on which the routing starts (e.g. 20200915)
    :type date: int
    :param start_time: Time to start the routing (in seconds of the day)
    :type start_time: int
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    urmo_ac_request = (
        "java -jar -Xmx12g {current_path}/urmoacjar/UrMoAC.jar "
        '--from "file;{home_directory}/.ptac/origins.csv" '
        "--shortest "
        '--to "file;{home_directory}/.ptac/destinations.csv" '
        "--mode foot "
        "--time {start_time} "
        "--epsg {epsg} "
        '--nm-output "file;{home_directory}/.ptac/sdg_output_{timestamp}.csv" '
        "--verbose "
        "--threads {number_of_threads} "
        "--dropprevious "
        "--date {date} "
        '--net "file;{home_directory}/.ptac/network.csv"'.format(
            home_directory=home_directory,
            timestamp=timestamp,
            current_path=current_path,
            epsg=epsg,
            number_of_threads=number_of_threads,
            date=date,
            start_time=int(start_time),
        )
    )

    return urmo_ac_request


def distance_to_closest(
    start_geometries,
    destination_geometries,
    network_gdf=None,
    boundary_geometries=None,
    transport_system=None,
    maximum_distance=None,
    start_time=35580,
    number_of_threads=1,
    date=20200915,
    verbose=0,
):
    """
    Python wrapper for UrMoAC Accessibility Calculator.

    :param network_gdf: Network dataset to use
    (optional, if None is provided dataset will be downloaded from osm automatically)
    :type network_gdf: Geopandas.GeoDataFrame::POLYGON
    :param start_geometries: Starting points for accessibility calculation
    :type start_geometries: Geopandas.GeoDataFrame::POLYGON
    :param destination_geometries: Starting point for accessibility calculation
    :type destination_geometries: Geopandas.GeoDataFrame::POLYGON
    :param boundary_geometries: Boundary dataset of the desired area
    :type boundary_geometries: Geopandas.GeoDataFrame::POLYGON
    :param maximum_distance: Maximum distance to next pt station (optional)
    :type maximum_distance: int
    :param start_time: Time to start the routing (in seconds of the day)
    :type start_time: int
    :param transport_system: Low-capacity or high-capacity pt system
    :type transport_system: str
    :param number_of_threads: The number of threads to use
    :type number_of_threads: int
    :param date: date on which the routing starts (e.g. 20200915) (not implemented yet)
    :type date: int
    :param verbose: The degree of verbosity. Valid values are 0 (silent) - 3 (debug)
    :type verbose: int
    :return accessibility_output: A geo data frame consists of accessibility calculation outputs
    :rtype: Geopandas.GeoDataFrame::POINT
    """
    start = timeit.default_timer()
    timestamp = int(round(time.time()))
    start_geometries = util.project_gdf(start_geometries, to_latlong=True)
    destination_geometries = util.project_gdf(destination_geometries, to_latlong=True)

    start_geometries = util.project_gdf(start_geometries, to_latlong=False)
    destination_geometries = util.project_gdf(destination_geometries, to_latlong=False)

    if not os.path.exists(f"{home_directory}/.ptac"):
        os.makedirs(f"{home_directory}/.ptac")

    if boundary_geometries is None:
        boundary_geometries = gpd.GeoDataFrame(
            index=[0], crs="epsg:4326", geometry=[start_geometries.unary_union]
        )

    if not boundary_geometries.crs == settings.default_crs:
        boundary_geometries = boundary_geometries.to_crs(settings.default_crs)

    if network_gdf is None:
        prepare_network(network_gdf=None, boundary=boundary_geometries, verbose=verbose)

    else:
        network_gdf = util.project_gdf(network_gdf, to_latlong=True)
        network_gdf = util.project_gdf(network_gdf, to_latlong=False)
        prepare_network(
            network_gdf=network_gdf, boundary=boundary_geometries, verbose=verbose
        )

    if "index" in start_geometries.columns:
        del start_geometries["index"]
    if "index" in destination_geometries.columns:
        del destination_geometries["index"]

    # generate unique ids for origins and destinations
    start_geometries = start_geometries.reset_index()
    destination_geometries = destination_geometries.reset_index()

    # write origins and destinations to disk
    prepare_origins_and_destinations(destination_geometries, od="destination")
    prepare_origins_and_destinations(start_geometries, od="origin")

    epsg = destination_geometries.crs.to_epsg()
    # build UrMoAC request
    urmo_ac_request = build_request(
        epsg=epsg, number_of_threads=number_of_threads, date=date, start_time=start_time, timestamp=timestamp
    )
    if verbose > 0:
        print("Starting UrMoAC to calculate accessibilities\n")
    if verbose > 1:
        print(f"UrMoAC request: {urmo_ac_request}\n")

    # Use UrMoAc to calculate SDG indicator
    os.system(urmo_ac_request)

    # read UrMoAC output
    header_list = ["o_id", "d_id", "avg_distance", "avg_tt", "avg_num", "avg_value"]
    output = pd.read_csv(
        f"{home_directory}/.ptac/sdg_output_{timestamp}.csv", sep=";", header=0, names=header_list
    )

    # only use distance on road network
    output["distance_pt"] = output["avg_distance"]
    output = output[["o_id", "d_id", "distance_pt"]]

    # Merge output to starting geometries
    accessibility_output = start_geometries.merge(
        output, how="left", left_on="index", right_on="o_id"
    )

    # Subset accessibility results based on transport system type or maximum distance
    accessibility_output = subset_result(
        accessibility_output,
        transport_system=transport_system,
        maximum_distance=maximum_distance,
    )
    stop = timeit.default_timer()

    print(f"calculation finished in {stop - start} seconds")
    clear_directory()
    return accessibility_output


def subset_result(accessibility_output, transport_system=None, maximum_distance=None):
    """
    Subset accessibility results based on transport system type or maximum distance.

    :param accessibility_output: A geo data frame consists of accessibility calculation outputs
    :type: Geopandas.GeoDataFrame::POINT
    :param transport_system: Low-capacity or high-capacity pt system
    :type transport_system: str
    :param maximum_distance: Maximum walkable distance
    :type maximum_distance: int
    :return accessibility_output: A geo data frame consists of accessibility calculation outputs based on
    the type of defined transport system
    :rtype: Geopandas.GeoDataFrame::POINT
    """
    if transport_system is not None and maximum_distance is not None:
        print("please indicate either transport_system or maximum_distance. Not both")
        sys.exit()
    if maximum_distance is not None:
        accessibility_output = accessibility_output[
            (accessibility_output["distance_pt"] <= maximum_distance)
        ]
    if transport_system is not None:
        if transport_system == "low-capacity":
            accessibility_output = accessibility_output[
                (accessibility_output["distance_pt"] <= 500)
            ]
        elif transport_system == "high-capacity":
            accessibility_output = accessibility_output[
                (accessibility_output["distance_pt"] <= 1000)
            ]
        else:
            print(
                "there is no such transport system. Please indicate either None, 'low-capacity' or 'high-capacity'"
            )
            sys.exit()
    return accessibility_output


def calculate_sdg(df_pop_total, pop_accessible, population_column, verbose=0):
    """
    Calculate sdg 11.2.1 value.

    :param df_pop_total: Population points GeoDataFrame (start geometries)
    :type df_pop_total: Geopandas.GeoDataFrame::POINT
    :param pop_accessible: A geo dataframe or a list of two geo dataframes consists of accessibility calculation outputs
    :type pop_accessible: Geopandas.GeoDataFrame::POINT
    :param population_column: The name of the population column in accessibility output dataframe
    :type: str
    :return SDG 11.2.1 indicator: SDG 11.2.1 indicator
    :rtype: int
    """
    total_population = df_pop_total[population_column].sum()
    # if input is a list of dataframes (low- and high-capacity transit systems):
    if isinstance(pop_accessible, list):
        if (population_column not in df_pop_total.columns) or (
            population_column not in pop_accessible[0]
        ):
            print(
                f"column {population_column} does not exist in both population datasets"
            )
            sys.exit()

        # concatenate dataframes
        df = pd.concat(pop_accessible)
        # drop duplicates:
        df = df.drop_duplicates(subset=["index", "o_id"])
        # sum population of accessibility output:
        accessibility_output_population = df[population_column].sum()
        if verbose < 0:
            print("Calculating SDG 11.2. indicator ... ")
        # calculate sdg 11.2.1 indicator by dividing population
        # of accessibility calculation result with total population:
        sdg = accessibility_output_population / total_population
        print("SDG 11.2.1 indicator is calculated")
    # if input is a single dataframe:
    else:
        if (population_column not in df_pop_total.columns) or (
            population_column not in pop_accessible
        ):
            print(
                f"column {population_column} does not exist in both population datasets"
            )
            sys.exit()
        # sum population of accessibility output:
        accessibility_output_population = pop_accessible[population_column].sum()
        print("Calculating SDG 11.2. indicator ... ")
        # calculate sdg 11.2.1 indicator by dividing population
        # of accessibility calculation result with total population:
        sdg = accessibility_output_population / total_population
        # print("SDG 11.2.1 indicator is calculated")
    return sdg
