#!/usr/bin/env python3
# coding:utf-8

"""Prepares dataset for accessibility computation and computes walking accessibilities from residential areas to public transport stops."""

"""
@name : accessibility.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021 12:44
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt
"""

import os
import sys
import geopandas as gpd
import ptac.osm as osm
import ptac.settings as settings
import ptac.util as util
import timeit
import datetime
from pathlib import Path
import pandas as pd
import glob


global home_directory
home_directory = Path.home()

global process_id
process_id = os.getpid()

def clear_directory(folder=f"{home_directory}/.ptac"):
    files = glob.glob(f"{folder}/{process_id}_*.csv")
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def prepare_origins_and_destinations(dest_gdf, od="origin"):
    """
        prepares origin or desination data set for usage in UrMoAC

        :param dest_gdf: origin or destination point data set (must be projected in UTM Projection)
        :type dest_gdf: Geopandas.GeoDataFrame:POINT
        :param od: indicate if "origin" or "destination"
        :type od: String
    """

    dest_gdf["x"] = dest_gdf.geometry.centroid.x
    dest_gdf["y"] = dest_gdf.geometry.centroid.y
    dest_gdf = dest_gdf[["x", "y"]]
    if od == "origin":
        dest_gdf = dest_gdf.dropna()
        dest_gdf.to_csv(f"{home_directory}/.ptac/{process_id}_origins.csv", sep=";", header=False)
    if od == "destination":
        dest_gdf.to_csv(f"{home_directory}/.ptac/{process_id}_destinations.csv", sep=";", header=False)


def prepare_network(network_gdf=None, boundary=None, verbose=0):
    """
        Loads road network from OpenStreetMap and prepares network for usage in UrMoAC

        :param network_gdf: network dataset to use (optional, if None is provided dataset will be downloaded from osm automatically)
        :param boundary: boundary of area where to download network (must be projected in WGS84)
        :type boundary: Geopandas.GeoDataFrame:POLYGON
        :param epsg: EPSG code of UTM projection for the area of interest
        :type epsg: Integer
        :param verbose: The degree of verbosity. Valid values are 0 (silent) - 3 (debug)
        :type verbose: Integer

    """

    if network_gdf is None:
        if verbose > 0:
            print("No street network was specified. Loading osm network..\n")
        network_gdf = osm.get_network(boundary)
        network_gdf = util.project_gdf(network_gdf, to_latlong=False)

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
    network_gdf = network_gdf.rename(columns={"u": "fromnode",
                                              "v": "tonode",
                                              "maxspeed": "vmax_osm",
                                              "highway": "street_type",
                                              "lanes": "lanes_osm",
                                              "index": "oid",
                                              })

    network_gdf = network_gdf.merge(network_characteristics, on="street_type", how="left")
    network_gdf = network_gdf.reset_index()
    network_gdf = network_gdf[["index",
                               "fromnode",
                               "tonode",
                               "mode_walk",
                               "mode_bike",
                               "mode_mit",
                               "vmax",
                               "length",
                               "geometry"]]
    network_gdf = pd.concat([network_gdf, network_gdf.geometry.bounds], axis=1)
    del network_gdf["geometry"]
    network_gdf.to_csv(f"{home_directory}/.ptac/{process_id}_network.csv", sep=";", header=False, index=False)
    # return network_gdf


def build_request(epsg, number_of_threads, date, start_time):
    """
        Builds requests for the UrMoAC

        :param epsg: PSG code of UTM projection for a certain area of interest
        :type epsg: String
        :param number_of_threads: PSG code of UTM projection for a certain area of interest
        :type number_of_threads: String
        :param date: date on which the routing starts (e.g. 20200915)
        :type date: integer
        :param start_time: time to start the routing (in seconds of the day)
        :type start_time: Integer

    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    urmo_ac_request = 'java -jar -Xmx12g {current_path}/urmoacjar/UrMoAccessibilityComputer-0.1-PRERELEASE-shaded.jar ' \
                      '--from file;"{home_directory}/.ptac/{process_id}_origins.csv" ' \
                      '--shortest ' \
                      '--to file;"{home_directory}/.ptac/{process_id}_destinations.csv" ' \
                      '--mode foot ' \
                      '--time {start_time} ' \
                      '--epsg {epsg} ' \
                      '--ext-nm-output "file;{home_directory}/.ptac/{process_id}_sdg_output.csv" ' \
                      '--verbose ' \
                      '--threads {number_of_threads} ' \
                      '--dropprevious ' \
                      '--date {date} ' \
                      '--net "file;{home_directory}/.ptac/{process_id}_network.csv"'.format(
        home_directory=home_directory,
        current_path=current_path,
        epsg=epsg,
        number_of_threads=number_of_threads,
        date=date,
        start_time=int(start_time),
        process_id=process_id
    )
    print(urmo_ac_request)
    return urmo_ac_request


def distance_to_closest(start_geometries,
                        destination_geometries,
                        network_gdf=None,
                        boundary_geometries=None,
                        transport_system=None,
                        maximum_distance=None,
                        start_time=35580,
                        number_of_threads=1,
                        date=20200915,
                        verbose=0):
    """
        Python wrapper for UrMoAC Accessibility Calculator

        :param network_gdf: network dataset to use (optional, if None is provided dataset will be downloaded from osm automatically)
        :type network_gdf: Geopandas.GeoDataFrame::POLYGON
        :param start_geometries: Starting points for accessibility calculation
        :type start_geometries: Geopandas.GeoDataFrame::POLYGON
        :param destination_geometries: Starting point for accessibility calculation
        :type destination_geometries: Geopandas.GeoDataFrame::POLYGON
        :param boundary_geometries:
        :type boundary_geometries: Geopandas.GeoDataFrame::POLYGON
        :param maximum_distance: Maximum distance to next pt station (optional)
        :rtype maximum_distance: Integer
        :param start_time: time to start the routing (in seconds of the day)
        :type start_time: Integer
        :param transport_system:
        :type transport_system:
        :param number_of_threads:
        :type number_of_threads: Integer
        :param date:
        :type date:
        :param verbose: The degree of verbosity. Valid values are 0 (silent) - 3 (debug)
        :type verbose:
        :return: A geo data frame consists of accessibility calculation outputs
        :rtype: Geopandas.GeoDataFrame::POINT
    """

    # todo: check if dataset is geographic coordinate system, if yes get epsg code of corresponding utm projection

    start = timeit.default_timer()

    start_geometries = util.project_gdf(start_geometries, to_latlong=True)
    destination_geometries = util.project_gdf(destination_geometries, to_latlong=True)

    start_geometries = util.project_gdf(start_geometries, to_latlong=False)
    destination_geometries = util.project_gdf(destination_geometries, to_latlong=False)

    if not os.path.exists(f"{home_directory}/.ptac"):
        os.makedirs(f"{home_directory}/.ptac")

    if boundary_geometries is None:
        boundary_geometries = gpd.GeoDataFrame(index=[0], crs='epsg:4326',
                                        geometry=[start_geometries.unary_union.convex_hull])

    if not boundary_geometries.crs == settings.default_crs:
        boundary_geometries = boundary_geometries.to_crs(settings.default_crs)

    if network_gdf is None:
        prepare_network(network_gdf=None, boundary=boundary_geometries, verbose=verbose)

    else:
        network_gdf = util.project_gdf(network_gdf, to_latlong=True)
        network_gdf = util.project_gdf(network_gdf, to_latlong=False)
        prepare_network(network_gdf=network_gdf, boundary=boundary_geometries, verbose=verbose)

    if "index" in start_geometries.columns:
        del start_geometries["index"]
    if "index" in destination_geometries.columns:
        del start_geometries["index"]

    # generate unique ids for origins and destinations
    start_geometries.reset_index(inplace=True)
    destination_geometries.reset_index(inplace=True)

    # write origins and destinations to disk
    prepare_origins_and_destinations(destination_geometries, od="destination")
    prepare_origins_and_destinations(start_geometries, od="origin")

    epsg = destination_geometries.crs.to_epsg()
    # build UrMoAC request
    urmo_ac_request = build_request(epsg=epsg, number_of_threads=number_of_threads, date=date, start_time=start_time)
    if verbose > 0:
        print("Starting UrMoAC to calculate accessibilities\n")
    if verbose > 1:
        print(f"UrMoAC request: {urmo_ac_request}\n")

    # Use UrMoAc to calculate SDG indicator
    os.system(urmo_ac_request)

    # read UrMoAC output
    header_list = ["o_id", "d_id", "avg_distance", "avg_tt", "avg_v", "avg_num", "avg_value", "avg_kcal", "avg_price",
                   "avg_co2", "avg_interchanges", "avg_access", "avg_egress", "avg_waiting_time",
                   "avg_init_waiting_time", "avg_pt_tt", "avg_pt_interchange_time", "modes"]

    output = pd.read_csv(f"{home_directory}/.ptac/{process_id}_sdg_output.csv", sep=";", header=0, names=header_list)

    # only use distance on road network (eliminate access and egress)
    output['distance_pt'] = output["avg_distance"] - output["avg_access"] - output["avg_egress"]
    output = output[["o_id", "d_id", "avg_access", "avg_egress", "distance_pt"]]

    # Merge output to starting geometries
    accessibility_output = start_geometries.merge(output,
                                                  how="left",
                                                  left_on="index",
                                                  right_on="o_id")

    # Subset starting points based on transport system type or maximum distance
    accessibility_output = subset_result(accessibility_output,
                                         transport_system=transport_system,
                                         maximum_distance=maximum_distance)
    stop = timeit.default_timer()

    print(f"calculation finished in {stop - start} seconds")
    clear_directory()
    return accessibility_output


def subset_result(accessibility_output, transport_system=None, maximum_distance=None):
    """
        :param accessibility_output:
        :param transport_system:
        :param maximum_distance:
        :return accessibility_output:
        :rtype: Geopandas.GeoDataFrame::POINT
    """

    if transport_system is not None and maximum_distance is not None:
        print("please indicate either transport_system or maximum_distance. Not both")
        sys.exit()
    if maximum_distance is not None:
        accessibility_output = accessibility_output[(accessibility_output["distance_pt"] <= maximum_distance)]
    if transport_system is not None:
        if transport_system == "low-capacity":
            accessibility_output = accessibility_output[(accessibility_output["distance_pt"] <= 500)]
        elif transport_system == "high-capacity":
            accessibility_output = accessibility_output[(accessibility_output["distance_pt"] <= 1000)]
        else:
            print("there is no such transport system. Please indicate either None, 'low-capacity' or 'high-capacity'")
            sys.exit()
    return accessibility_output


def calculate_sdg(df_pop_total, pop_accessible, population_column, verbose=0):
    """

        :param df_pop_total:
        :param pop_accessible:
        :param population_column:
        :return SDG 11.2.1 indicator:
        :rtype: Integer

    """
    total_population = df_pop_total[population_column].sum()
    # if input is a list of dataframes (low- and high-capacity transit systems):
    if isinstance(pop_accessible, list):
        if (population_column not in df_pop_total.columns) or (population_column not in pop_accessible[0]):
            print(f"column {population_column} does not exist in both population datasets")
            sys.exit()

        # concatenate dataframes
        df = pd.concat(pop_accessible)
        # drop duplicates:
        df = df.drop_duplicates(subset=['index', 'o_id'])
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
        if (population_column not in df_pop_total.columns) or (population_column not in pop_accessible):
            print(f"column {population_column} does not exist in both population datasets")
            sys.exit()
        # sum population of accessibility output:
        accessibility_output_population = pop_accessible[population_column].sum()
        print("Calculating SDG 11.2. indicator ... ")
        # calculate sdg 11.2.1 indicator by dividing population
        # of accessibility calculation result with total population:
        sdg = accessibility_output_population / total_population
        print("SDG 11.2.1 indicator is calculated")
    return sdg

