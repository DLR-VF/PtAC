import sys
import os
#print(os.path.abspath('..'))
#sys.path.insert(0, os.path.abspath('..'))
#print(sys.path)
import PtAC.osm as osm
import PtAC.urbanspatialio as io
import PtAC.util as util
import PtAC.settings as settings

from sqlalchemy import create_engine
import timeit
import pandas as pd
import geopandas as gpd
import osmnx as ox
import shutil


def distance_to_closest(db_access,
                        start_geometries, 
                        facility=None, 
                        epsg=None, 
                        destination_geometries=None, 
                        network_table=None, 
                        boundary_geometries=None, 
                        city=None, 
                        start_time=35580, 
                        maximum_distance=500, 
                        mode="foot", 
                        gtfs_schema=None, 
                        gtfs_prefix="", 
                        number_of_threads=4, 
                        date=20200915, 
                        weighting_column=None, 
                        transport_system=None,
                        verbose=0):
    """
        Python wrapper for UrMoAC Accessibility Calculator

        :param conn: db connection
        :type conn: sqlalchemy connection
        :param start_geometries: Starting point for accessibility calculation (can be either point or polygon)
        :type start_geometries: Geopandas.GeoDataFrame::POLYGON (must be in UTM coordinates)
        :param facility: facilities to calculate accessibilities (options are: "restaurant","park", more to come..)
        :type facility: String
        :param boundary_geometries: area to search for facilities
        :type boundary_geometries: geopandas.GeoDataFrame
        :param start_time: time to start the routing (in seconds of the day)
        :type start_time: Integer
        :param: travel_time: maximum travel time (in seconds)
        :type: travel_time: Integer
        :return: Aggregation geometries with accessibilities
        :type Geopandas.GeoDataFrame:POLYGON

        """
    start = timeit.default_timer()

    if facility is None and destination_geometries is None:
        print('Please indicate either osm facilities or destination geometries. '
              'Facilities can be "restaurant" or "park"')
        #sys.exit()

    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if boundary_geometries:
        boundary_geometries_copy = boundary_geometries.copy()
    start_geometries_copy = start_geometries.copy()
    if epsg:
        start_geometries_copy = start_geometries.to_crs(epsg) 
    else:
            # todo:fix this
        start_geometries_copy = util.project_gdf(start_geometries_copy)
    try:
        engine = create_engine('postgresql://{user_name}:{password}@{host}:5432/{db_name}'.format(user_name=db_access["user_name"],
                                                                                   password=db_access["password"],
                                                                                   host=db_access["host"],
                                                                                   db_name=db_access["db_name"])) 
        conn = engine.connect()
    except Exception as e:
        print(e)
        sys.exit()

    if boundary_geometries is None:
        boundary_geometries = start_geometries_copy.copy()
    if facility == "restaurant":
        if verbose > 0:
            print("Loading {facility}s from osm \n".format(facility=facility))
        facility_dict = settings.osm_restaurants_tags

    if facility == "park":
        if verbose > 0:
            print("Loading {facility}s from osm \n".format(facility=facility))
            # todo: remove points from park dataset?
        facility_dict = settings.osm_parks_tags

    if not boundary_geometries.crs.srs == "epsg:4326":
        boundary_geometries = boundary_geometries.to_crs(4326)
         
    boundary = boundary_geometries.unary_union.convex_hull

    if facility is not None:
        facility_df = osm.get_facility(boundary, facility=facility_dict)
        destination_df = facility_df.to_crs(start_geometries.crs)
            # io.to_postgis(destination_df, conn, schema=db_access["schema"], table_name=facility)

    else:
        destination_df = destination_geometries.to_crs(start_geometries.crs)
    facility = "destination_geometries"
    #print("destination_df.crs: ", destination_df.crs)
    io.to_postgis(destination_df, conn, schema=db_access["schema"], table_name=city + "_" + facility)

    if verbose > 0:
        print("importing {facility}..\n".format(facility=facility))
    query = [city, 1]
    gdf_place = ox.geocoder.geocode_to_gdf(query[0], which_result=query[1])
    boundary = gdf_place.unary_union
    if network_table == None:
        if verbose > 0:
            print("No street network was specified. Loading osm network..\n")
        
        network = osm.get_network(boundary)
        network_gdf = ox.graph_to_gdfs(network)[1]
        network_characteristics = settings.highways
        network_characteristics.reset_index(inplace=True)
        network_characteristics.rename(columns={"index": "street_type"}, inplace=True)

        network_gdf.reset_index(inplace=True)
        network_gdf["the_geom"] = network_gdf["geometry"]
        network_gdf = network_gdf.set_geometry("the_geom")
        del network_gdf["geometry"]
        network_gdf = network_gdf.rename(columns={"u": "nodefrom",
                                                  "v": "nodeto",
                                                  "maxspeed": "vmax_osm",
                                                  "highway": "street_type",
                                                  "lanes": "lanes_osm"})
                                                  # "index": "oid"})
        network_gdf["oid"] = network_gdf.index
        #print("network gdf after renaming: ", network_gdf.head())

        network_gdf["street_type"] = 'highway_' + network_gdf["street_type"].astype(str)
        network_gdf = network_gdf.merge(network_characteristics, on="street_type", how="left")
        network_table = "network_walk_unsimplified"

        if verbose > 0:
            print("importing network..\n".format(facility=facility))
        io.to_postgis(network_gdf, conn, schema=db_access["schema"], table_name=city + "_" + network_table, if_exists="replace") 

    boundary_geometries = boundary_geometries.to_crs(start_geometries_copy.crs)
    #boundary_geometries = boundary_geometries.to_crs('epsg:4326')
    if verbose > 0:
        print("importing start geometries..\n".format(facility=facility))

    start_geometries_copy = start_geometries_copy.to_crs('epsg:4326')
    io.to_postgis(start_geometries_copy, conn, schema=db_access["schema"], table_name=city + "_starting_geometries", if_exists="replace")

    boundary_gdf = gpd.GeoDataFrame(gpd.GeoSeries(boundary, crs=4326).to_crs(start_geometries_copy.crs))
    boundary_gdf = boundary_gdf.rename(columns={0: 'geometry'}).set_geometry('geometry')
    #print("boundary_gdf: ", boundary_gdf.crs)
    #print("boundary_geometries: ", boundary_geometries.crs)
    #boundary_gdf = boundary_gdf.to_crs('epsg:4326')
    io.to_postgis(boundary_geometries, conn, schema=db_access["schema"], table_name=city + "_from_aggregation_area", if_exists="replace")
    io.to_postgis(boundary_gdf, conn, schema=db_access["schema"], table_name=city + "_to_aggregation_area", if_exists="replace")
    
    print("Calculating the accessibilities..")

    if not gtfs_schema:
        urmo_ac_request = 'java -jar -Xmx12g UrMoAC.jar ' \
                          '--from "db;jdbc:postgresql://{host}/{db_name};{schema}.{from_table_name};{username};{psw}" ' \
                          '--from.id index --from.geom geometry ' \
                          '--from-filter "geometry!={null}" ' \
                          '--to "db;jdbc:postgresql://{host}/{db_name};{schema}.{to_table_name};{username};{psw}" ' \
                          '--to.id index ' \
                          '--to.geom geometry ' \
                          '--to-filter "geometry!={null}" ' \
                          '--mode {mode} ' \
                          '--time {start_time} ' \
                          '--epsg {epsg} ' \
                          '--shortest ' \
                          '--ext-nm-output "file;tmp/{city}_output_ext_{facility}.txt" ' \
                          '--verbose ' \
                          '--threads {number_of_threads} ' \
                          '--dropprevious ' \
                          '--date {date} ' \
                          '--net "db;jdbc:postgresql://{host}/{db_name};{schema}.{network_table};{username};{psw}"'.format(
            from_table_name=city + "_starting_geometries",
            network_table=city + network_table,
            #epsg=start_geometries_copy.crs.srs.split(":")[1],
            epsg=epsg,
            to_table_name= city + facility,
            facility=facility,
            mode=mode,
            city=city,
            username=db_access["user_name"],
            psw=db_access["password"],
            db_name=db_access["db_name"],
            schema=db_access["schema"],
            host=db_access["host"],
            number_of_threads=number_of_threads,
            date=date,
            start_time=int(start_time),
            null="'NULL'")

    #print(urmo_ac_request)
    os.system(urmo_ac_request)
    header_list = ["o_id", "d_id", "avg_distance", "avg_tt", "avg_v", "avg_num", "avg_value", "avg_kcal", "avg_price", "avg_co2", "avg_interchanges", 
                   "avg_access", "avg_egress", "avg_waiting_time", "avg_init_waiting_time", "avg_pt_tt", "avg_pt_interchange_time", "modes"]
    output = pd.read_csv("tmp/" + city + "_output_ext_{facility}.txt".format(facility=facility), sep=";", header=0, names=header_list)
    #print("output: ", output.head())
    if not facility is None:
        output = output.add_suffix("_{facility}".format(facility=facility))
    accessibility_output = start_geometries.merge(output, how="left", left_on="index", right_on="o_id_{facility}".format(facility=facility))#{facility}
    accessibility_output = accessibility_output[accessibility_output["o_id_{facility}".format(facility=facility)] != -1]
    stop = timeit.default_timer()
    #if verbose > 0:
        #print("accessibility calculated in {exec_time} seconds".format(exec_time=round(stop - start)))
  
    accessibility_output['average_distance'] = accessibility_output["avg_distance_destination_geometries"] \
                              - accessibility_output["avg_access_destination_geometries"] \
                              - accessibility_output["avg_egress_destination_geometries"]
    if verbose > 0:
        if transport_system == None:
            accessibility_output = accessibility_output
            print("accessibility to public transport calculated in {exec_time} seconds".format(exec_time=round(stop - start)))
        if transport_system == "low-capacity":
            accessibility_output = accessibility_output[(accessibility_output["average_distance"] <= 500)]
            stop = timeit.default_timer()
            print("accessibility to {transport_system} public transport within 500 m calculated in {exec_time} seconds".format(transport_system=transport_system, exec_time=round(stop - start)))
        if transport_system == "high-capacity":
            accessibility_output = accessibility_output[(accessibility_output["average_distance"] <= 1000)]
            stop = timeit.default_timer()
            print("accessibility to {transport_system} public transport within 1 km calculated in {exec_time} seconds".format(transport_system=transport_system, exec_time=round(stop - start)))
    return accessibility_output

def calculate_sdg(total_population, accessibility_output_population):
    print("Calulating SDG 11.2. indicator ... ")
    sdg = accessibility_output_population/ total_population
    print("SDG 11.2. indicator is calculated ")
    return sdg

