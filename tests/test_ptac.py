"""
Unit tests for PtAC library
"""

import unittest
import geopandas as gpd
import ptac.accessibility as accessibility
import ptac.population as population
import ptac.osm as osm
import ptac.util as util
import pathlib
from pathlib import Path
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# print(THIS_DIR)

# define queries to use throughout tests
location_point = (37.791427, -122.410018)

# inheriting from unittest. TestCase gives access to a lot of different testing capabilities within the class
class PtACTest(unittest.TestCase):
    def set_up(self):
        self.data_path = str(pathlib.Path(__file__).parent.absolute())
        self.pt = gpd.read_file(self.data_path + "/input_data/pt_example.gpkg")#.copy()
        #print(self.pt["osmid"].count())
        self.pt_low = gpd.read_file(self.data_path + "/input_data/pt_low_example.gpkg")#.copy()
        self.pt_high = gpd.read_file(self.data_path + "/input_data/pt_high_example.gpkg")#.copy()
        #print("count pt_low: ", self.pt_low["osmid"].count())
        #print("count pt_high: ", self.pt_high["osmid"].count())
        self.pop = gpd.read_file(self.data_path + "/input_data/population_example.gpkg")#.copy()
        #print("sum pop: ", self.pop["pop"].sum())
        self.net = gpd.read_file(self.data_path + "/input_data/net_example.gpkg")#.copy()
        #print("count network: ", self.net["osmid"].count())
        self.boundary = gpd.read_file(self.data_path + "/input_data/boundary_example.gpkg")
        #self.boundary = gpd.GeoDataFrame(
        #    index=[0], crs="epsg:4326", geometry=[self.pop.unary_union]
        #)
        #self.net = osm.get_network(self.boundary)
        self.raster = self.data_path + "/input_data/friedrichshain_raster.tif"

    def test_prepare_network(self):
        self.set_up()
        df_prepare_network = accessibility.prepare_network(network_gdf=None, boundary=self.boundary)
        value = df_prepare_network["osmid"].count()
        expected_value = 59432
        self.assertEqual(value, expected_value)

    def test_get_network(self):
        self.set_up()
        df_osm_network = osm.get_network(polygon=self.boundary, network_type="walk", custom_filter=None, verbose=0)
        value = df_osm_network["index"].count()
        expected_value = 59432
        self.assertEqual(value, expected_value)

    def test_dist_to_closest_max_dist(self):
        self.set_up()
        value = accessibility.distance_to_closest(
            self.pop,
            self.pt,
            network_gdf=self.net,
            maximum_distance=500,
        )["pop"].sum()
        print(value)
        value2 = accessibility.distance_to_closest(
            self.pop,
            self.pt,
            network_gdf=None,
            boundary_geometries=self.boundary,
            maximum_distance=500,
        )["pop"].sum()
        print(value2)
        expected_value = 84902
        self.assertEqual(round(value), expected_value)
        self.assertEqual(round(value2), expected_value)

    def test_dist_to_closest_transport_system(self):
        self.set_up()
        value_low = accessibility.distance_to_closest(
            self.pop,
            self.pt_low,
            network_gdf=self.net,
            transport_system="low-capacity"
        )["pop"].sum()
        print(value_low)
        value_low2 = accessibility.distance_to_closest(
            self.pop,
            self.pt_low,
            network_gdf=None,
            boundary_geometries=self.boundary,
            transport_system="low-capacity",
        )["pop"].sum()
        print(value_low2)
        expected_value_low = 67933
        self.assertEqual(round(value_low), expected_value_low)
        self.assertEqual(round(value_low2), expected_value_low)

        value_high = accessibility.distance_to_closest(
            self.pop,
            self.pt_high,
            network_gdf=self.net,
            transport_system="high-capacity",
        )["pop"].sum()
        value_high2 = accessibility.distance_to_closest(
            self.pop,
            self.pt_high,
            network_gdf=None,
            boundary_geometries=self.boundary,
            transport_system="high-capacity",
        )["pop"].sum()
        expected_value_high = 83298
        self.assertEqual(round(value_high), expected_value_high)
        self.assertEqual(round(value_high2), expected_value_high)

    def test_calculate_sdg(self):
        self.set_up()
        value_access_low = accessibility.distance_to_closest(
            self.pop,
            self.pt_low,
            network_gdf=self.net,
            transport_system="low-capacity"
        )
        value_access_high = accessibility.distance_to_closest(
            self.pop,
            self.pt_high,
            network_gdf=self.net,
            transport_system="high-capacity",
        )
        value = self.pop
        result = accessibility.calculate_sdg(
            value, [value_access_low, value_access_high], population_column="pop"
        )
        expected_result = 0.9913
        self.assertEqual(round(result, 4), expected_result)

    def test_raster_to_points(self):
        self.set_up()
        # value = ((population.raster_to_points(self.raster))["geometry"].type == "Point")
        value = population.raster_to_points(self.raster)
        value = float(value["pop"].sum())
        expected_value = 88270.71
        self.assertEqual(round(value, 2), expected_value)

    def test_project_gdf(self):
        self.set_up()
        value = util.project_gdf(
            gdf=self.pop, geom_col="geometry", to_crs=None, to_latlong=False
        ).crs
        expected_value = "epsg:32633"
        self.assertEqual(value, expected_value)


if __name__ == "__main__":
    unittest.main()
