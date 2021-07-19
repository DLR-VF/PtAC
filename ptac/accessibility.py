
import os
import ptac.osm as osm
import ptac.settings as settings
import timeit
import pandas as pd
import osmnx as ox

import sys


#sys.path.insert(0, os.path.abspath('..'))
import numpy as np
import rasterio
from affine import Affine
import geopandas as gpd

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
        dest_gdf.to_csv("tmp/origins.csv", sep=";", header=False)
    if od == "destination":
        dest_gdf.to_csv("tmp/destinations.csv", sep=";", header=False)


def prepare_network(boundary, epsg, verbose=0):
    """
        Loads road network from OpenStreetMap and prepares network for usage in UrMoAC

        :param boundary: boundary of area where to download network (must be projected in WGS84)
        :type boundary: Geopandas.GeoDataFrame:POLYGON
        :param epsg: EPSG code of UTM projection for the area of interest
        :type epsg: Integer
        :param verbose: The degree of verbosity. Valid values are 0 (silent) - 3 (debug)
        :type verbose: Integer

    """
    if verbose > 0:
        print("No street network was specified. Loading osm network..\n")
    network = osm.get_network(boundary)
    network_gdf = ox.graph_to_gdfs(network)[1]
    network_gdf = network_gdf.to_crs(epsg)
    network_characteristics = settings.highways
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

    network_gdf["street_type"] = 'highway_' + network_gdf["street_type"].astype(str)
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
    network_gdf.to_csv("tmp/network.csv", sep=";", header=False, index=False)
    #return network_gdf


def build_request(epsg, number_of_threads,
                  date, start_time):
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
    urmo_ac_request = f'java -jar -Xmx12g {current_path}/UrMoAccessibilityComputer-0.1-PRERELEASE-shaded.jar ' \
                      '--from file;"tmp/origins.csv" ' \
                      '--shortest ' \
                      '--to file;"tmp/destinations.csv" ' \
                      '--mode foot ' \
                      f'--time {int(start_time)} ' \
                      f'--epsg {epsg} ' \
                      '--ext-nm-output "file;tmp/sdg_output.txt" ' \
                      '--verbose ' \
                      f'--threads {number_of_threads} ' \
                      '--dropprevious ' \
                      f'--date {date} ' \
                      '--net "file;tmp/network.csv"'
    return urmo_ac_request

def transport_system_function(accessibility_output, start, transport_system, maximum_distance):
    if transport_system is None and maximum_distance is None:
        accessibility_output = accessibility_output["distance_pt"]
        stop = timeit.default_timer()
        print(f"accessibility to public transport stops calculated in {round(stop - start)} seconds")
    if transport_system is None and maximum_distance is not None:
        accessibility_output = accessibility_output[(accessibility_output["distance_pt"] <= maximum_distance)]
        stop = timeit.default_timer()
        print(f"accessibility to public transport stops within {maximum_distance} m calculated in {round(stop - start)} seconds")
    if transport_system is not None:
        if transport_system == "low-capacity":
            accessibility_output = accessibility_output[(accessibility_output["distance_pt"] <= 500)]
            stop = timeit.default_timer()
            print(f"accessibility to public transport stops within 500 m calculated in {round(stop - start)} seconds")
        elif transport_system == "high-capacity":
            accessibility_output = accessibility_output[(accessibility_output["distance_pt"] <= 1000)]
            stop = timeit.default_timer()
            print(f"accessibility to public transport stops within 1000 m calculated in {round(stop - start)} seconds")
        else:
            print("there is no such transport system")

    return accessibility_output

def distance_to_closest(start_geometries,
                        destination_geometries=None,
                        epsg=None,
                        network_exists=False,
                        boundary_geometries=None,
                        start_time=35580,
                        transport_system=None,
                        maximum_distance=None,
                        number_of_threads=4,
                        date=20200915,
                        verbose=0):
    """
        Python wrapper for UrMoAC Accessibility Calculator

        :param start_geometries: Starting points for accessibility calculation
        :type start_geometries: Geopandas.GeoDataFrame::POLYGON
        :param destination_geometries: Starting point for accessibility calculation
        :type destination_geometries: Geopandas.GeoDataFrame::POLYGON
        :param epsg: EPSG code of UTM projection for a certain area of interest
        :type epsg: String
        :param network_exists:
        :type network_exists: Boolean
        :param boundary_geometries:
        :type boundary_geometries: Geopandas.GeoDataFrame::POLYGON
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
        """

    start = timeit.default_timer()

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    if not boundary_geometries.crs == "epsg:4326":
        boundary_geometries = boundary_geometries.to_crs(4326)

    boundary = boundary_geometries.unary_union.convex_hull

    if network_exists is False:
        prepare_network(boundary, epsg, verbose)

    if "index" in start_geometries.columns:
        del start_geometries["index"]
    if "index" in destination_geometries.columns:
        del destination_geometries["index"]

    # generate unique ids for origins and destinations
    start_geometries.reset_index(inplace=True)
    destination_geometries.reset_index(inplace=True)

    # transform origins and destinations to utm coordinates
    destination_geometries = destination_geometries.to_crs(epsg)
    start_geometries = start_geometries.to_crs(epsg)

    # write origins and destinations to disk
    prepare_origins_and_destinations(destination_geometries, od="destination")
    prepare_origins_and_destinations(start_geometries, od="origin")

    # build UrMoAC request
    urmo_ac_request = build_request(epsg=epsg, number_of_threads=number_of_threads, date=date, start_time=start_time)
    if verbose > 0:
        print("Starting UrMoAC to calculate accessibilities\n")
        #print(f"UrMoAC request: {urmo_ac_request}\n")

    # Use UrMoAc to calculate SDG indicator
    os.system(urmo_ac_request)

    # read UrMoAC output
    header_list = ["o_id", "d_id", "avg_distance", "avg_tt", "avg_v", "avg_num", "avg_value", "avg_kcal", "avg_price",
                   "avg_co2", "avg_interchanges", "avg_access", "avg_egress", "avg_waiting_time",
                   "avg_init_waiting_time", "avg_pt_tt", "avg_pt_interchange_time", "modes"]

    output = pd.read_csv("tmp/sdg_output.txt", sep=";", header=0, names=header_list)

    # Merge output to starting geometries
    accessibility_output = start_geometries.merge(output,
                                                  how="left",
                                                  left_on="index",
                                                  right_on="o_id")

    # do not take into account access and egress distances. this might not be necessary any more..
    accessibility_output['distance_pt'] = accessibility_output["avg_distance"] \
                                                - accessibility_output["avg_access"] \
                                                - accessibility_output["avg_egress"]

    if verbose > 0:

        accessibility_output = transport_system_function(accessibility_output,
                                                         start=start, transport_system=transport_system,
                                                         maximum_distance=maximum_distance)
    return accessibility_output

def concat_dfs(input):
    if isinstance(input, list):
        # concatenate dataframes
        df = pd.concat(input)
        # drop duplicates:
        df = df.drop_duplicates(subset=['index', 'o_id'])
    return df

# calculate SDG 11.2.1 indicator: pass input either as one dataframe or a list of two dataframes
def calculate_sdg(population, input, population_column):
    total_population = population[population_column].sum()
    # if input is a list of dataframes (low- and high-capacity transit systems):
    if isinstance(input, list):
        # concatenate dataframes
        df = pd.concat(input)
        # drop duplicates:
        df = df.drop_duplicates(subset=['index', 'o_id'])
        # sum population of accessibility output:
        accessibility_output_population = df[population_column].sum()
        print("Calculating SDG 11.2. indicator ... ")
        # calculate sdg 11.2.1 indicator by dividing population
        # of accessibility calculation result with total population:
        sdg = accessibility_output_population / total_population
        print("SDG 11.2.1 indicator is calculated")
    # if input is a single dataframe:
    else:
        # sum population of accessibility output:
        accessibility_output_population = input[population_column].sum()
        print("Calculating SDG 11.2. indicator ... ")
        # calculate sdg 11.2.1 indicator by dividing population
        # of accessibility calculation result with total population:
        sdg = accessibility_output_population / total_population
        print("SDG 11.2.1 indicator is calculated")
    return sdg


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

# creates population dataset in gpkg, csv and shp file formats:
def create_population_data(input_path, output_path, extension):
    cities = os.listdir(rf'{input_path}')
    for city in cities:
        # print(city)
        if city.endswith("tif"):
            print(f"processing {city}")
            raster_path = rf'{input_path}/{city}'
            if extension == "gpkg":
                points_gdf = raster_to_points(raster_path, band=1, epsg=4326)
                city_name = city.split(".")[0].lower()
                points_gdf.to_file(f"{output_path}/{city_name}_pop_point.{extension}", driver="GPKG")
                print(f"{city} population points saved as {extension} file")
            elif extension == "shp":
                points_gdf = raster_to_points(raster_path, band=1, epsg=4326)
                city_name = city.split(".")[0].lower()
                points_gdf.to_file(f"{output_path}/{city_name}_pop_point.{extension}", driver="ESRI Shapefile")
                print(f"{city} population points saved as {extension} file")
            elif extension == "csv":
                points_gdf = raster_to_points(raster_path, band=1, epsg=4326)
                city_name = city.split(".")[0].lower()
                points_gdf.to_csv(f"{output_path}/{city_name}_pop_point.{extension}", sep=";", header=False)
                print(f"{city} population points saved as {extension} file")
            else:
                print(f"{extension} extension is not supported")


