import sys
import os
import PtAC.osm as osm
import PtAC.util as util
import PtAC.settings as settings
import timeit
import pandas as pd
import geopandas as gpd
import osmnx as ox


def prepare_origins_and_destinations(dest_gdf, od="origin"):

    dest_gdf["x"] = dest_gdf.geometry.centroid.x
    dest_gdf["y"] = dest_gdf.geometry.centroid.y
    dest_gdf = dest_gdf[["x", "y"]]
    if od == "origin":
        dest_gdf.dropna(inplace=True)
        dest_gdf.to_csv("tmp/origins.csv", sep=";", header=False)
    if od == "destination":
        dest_gdf.to_csv("tmp/destinations.csv", sep=";", header=False)


def prepare_network(boundary, crs, verbose=0):
    if verbose > 0:
        print("No street network was specified. Loading osm network..\n")
    network = osm.get_network(boundary)
    network_gdf = ox.graph_to_gdfs(network)[1]
    network_gdf = network_gdf.to_crs(crs)
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
    return network_gdf

def build_request(epsg, mode, number_of_threads,
                  date, start_time):
    urmo_ac_request = 'java -jar -Xmx12g UrMoAccessibilityComputer-0.1-PRERELEASE-shaded.jar ' \
                      '--from file;"tmp/origins.csv" '\
                      '--shortest '\
                      '--to file;"tmp/destinations.csv" ' \
                      '--mode {mode} ' \
                      '--time {start_time} ' \
                      '--epsg {epsg} ' \
                      '--nm-output "file;tmp/sdg_output.txt" ' \
                      '--verbose ' \
                      '--threads {number_of_threads} ' \
                      '--dropprevious ' \
                      '--date {date} ' \
                      '--net "file;tmp/network.csv"'.format(
        epsg=epsg,
        mode=mode,
        number_of_threads=number_of_threads,
        date=date,  # date_obj.date().strftime("%Y%m%d"),
        start_time=int(start_time),
        null="'NULL'")
    return urmo_ac_request



def distance_to_closest(start_geometries,
                        facility=None, 
                        epsg=None, 
                        destination_geometries=None, 
                        network_exists=False,
                        boundary_geometries=None, 
                        city=None, 
                        start_time=35580, 
                        maximum_distance=500, 
                        mode="foot",
                        number_of_threads=4, 
                        date=20200915,
                        transport_system=None,
                        verbose=0):
    """
        Python wrapper for UrMoAC Accessibility Calculator

        :param conn: db connection
        :type conn: sqlalchemy connection
        :param start_geometries: Starting point for accessibility calculation (can be either point or polygon)
        :type start_geometries: Geopandas.GeoDataFrame::POLYGON (must be in UTM coordinates)
        :param destination_geometries: Starting point for accessibility calculation (can be either point or polygon)
        :type destination_geometries: Geopandas.GeoDataFrame::POLYGON (must be in UTM coordinates)
        :param start_time: time to start the routing (in seconds of the day)
        :type start_time: Integer
        :param: travel_time: maximum travel time (in seconds)
        :type: travel_time: Integer
        :return: Aggregation geometries with accessibilities
        :type Geopandas.GeoDataFrame:POLYGON

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
        del start_geometries["index"]
    #generate unique ids for origins and destinations
    start_geometries.reset_index(inplace=True)
    destination_geometries.reset_index(inplace=True)

    destination_geometries = destination_geometries.to_crs(epsg)
    start_geometries = start_geometries.to_crs(epsg)
    prepare_origins_and_destinations(destination_geometries, od="destination")
    prepare_origins_and_destinations(start_geometries, od="origin")

    urmo_ac_request = build_request(epsg, mode,
                                    number_of_threads, date, start_time)
    print(urmo_ac_request)

    os.system(urmo_ac_request)
    header_list = ["o_id", "d_id", "avg_distance", "avg_tt", "avg_v", "avg_num"]

    output = pd.read_csv("tmp/sdg_output.txt", sep=";", header=0, names=header_list)

    accessibility_output = start_geometries.merge(output,
                                                  how="left",
                                                  left_on="index",
                                                  right_on="o_id".format(facility=facility))
    return accessibility_output
    # accessibility_output['average_distance'] = accessibility_output["avg_distance_destination_geometries"] \
    #                           - accessibility_output["avg_access_destination_geometries"] \
    #                           - accessibility_output["avg_egress_destination_geometries"]
    # if verbose > 0:
    #     if transport_system == None:
    #         accessibility_output = accessibility_output
    #         print("accessibility to public transport calculated in {exec_time} seconds".format(exec_time=round(stop - start)))
    #     if transport_system == "low-capacity":
    #         accessibility_output = accessibility_output[(accessibility_output["average_distance"] <= 500)]
    #         stop = timeit.default_timer()
    #         print("accessibility to {transport_system} public transport within 500 m calculated in {exec_time} seconds".format(transport_system=transport_system, exec_time=round(stop - start)))
    #     if transport_system == "high-capacity":
    #         accessibility_output = accessibility_output[(accessibility_output["average_distance"] <= 1000)]
    #         stop = timeit.default_timer()
    #         print("accessibility to {transport_system} public transport within 1 km calculated in {exec_time} seconds".format(transport_system=transport_system, exec_time=round(stop - start)))
    # return accessibility_output

def calculate_sdg(total_population, accessibility_output_population):
    print("Calulating SDG 11.2. indicator ... ")
    sdg = accessibility_output_population/ total_population
    print("SDG 11.2. indicator is calculated ")
    return sdg

