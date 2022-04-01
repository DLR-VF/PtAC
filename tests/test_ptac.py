"""
Unit tests for PtAC library
"""


import unittest
import geopandas as gpd
import osmnx as ox
import ptac.accessibility as accessibility
import ptac.population as population
import ptac.osm as osm
import pathlib

# define queries to use throughout tests
location_point = (37.791427, -122.410018)

# inheriting from unittest. TestCase gives access to a lot of different testing capabilities within the class
class PtACTest(unittest.TestCase):
    def set_up(self):
        self.data_path = str(pathlib.Path(__file__).parent.absolute())
        self.pt = gpd.read_file(self.data_path+"/input_data/pt_example.gpkg")
        self.pt_low = gpd.read_file(self.data_path+"/input_data/pt_low_example.gpkg")
        self.pt_high = gpd.read_file(self.data_path+"/input_data/pt_high_example.gpkg")
        self.pop = gpd.read_file(self.data_path+"/input_data/population_example.gpkg")
        self.net = gpd.read_file(self.data_path + "/input_data/net_example.gpkg")
        self.boundary = gpd.read_file(self.data_path + "/input_data/boundary_example.gpkg")
        self.raster = self.data_path + "/input_data/friedrichshain_raster.tif"

    def test_dist_to_closest_max_dist(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop,
                                                  self.pt,
                                                  network_gdf=self.net,
                                                  maximum_distance=500)["pop"].sum()
        value2 = accessibility.distance_to_closest(self.pop,
                                                   self.pt,
                                                   network_gdf=None,
                                                   boundary_geometries=self.boundary,
                                                   maximum_distance=500)["pop"].sum()
        print(value2)
        expected_value = 84819.55368244648
        self.assertEqual(value, expected_value)

    def test_dist_to_closest_transport_system(self):
        self.set_up()
        value_low = accessibility.distance_to_closest(self.pop,
                                                  self.pt_low,
                                                  network_gdf=self.net,
                                                  transport_system="low-capacity")["pop"].sum()
        value_low2 = accessibility.distance_to_closest(self.pop,
                                                   self.pt_low,
                                                   network_gdf=None,
                                                   boundary_geometries=self.boundary,
                                                   transport_system="low-capacity")["pop"].sum()
        expected_value_low = 67902.45639175177
        self.assertEqual(value_low, value_low2, expected_value_low)

        value_high = accessibility.distance_to_closest(self.pop,
                                                  self.pt_high,
                                                  network_gdf=self.net,
                                                  transport_system="high-capacity")["pop"].sum()
        value_high2 = accessibility.distance_to_closest(self.pop,
                                                   self.pt_high,
                                                   network_gdf=None,
                                                   boundary_geometries=self.boundary,
                                                   transport_system="high-capacity")["pop"].sum()
        expected_value_high = 83291.75091338158
        self.assertEqual(value_high, value_high2, expected_value_high)

    def test_calculate_sdg(self):
        self.set_up()
        value_access_low = accessibility.distance_to_closest(self.pop,
                                                             self.pt_low,
                                                             network_gdf=self.net,
                                                             transport_system="low-capacity")
        value_access_high = accessibility.distance_to_closest(self.pop,
                                                              self.pt_high,
                                                              network_gdf=self.net,
                                                              transport_system="high-capacity")
        value = self.pop
        result = accessibility.calculate_sdg(value, [value_access_low, value_access_high], population_column="pop")
        expected_result = 0.9855767281935321
        self.assertEqual(result, expected_result)

    def test_prepare_network(self):
        self.set_up()
        value = accessibility.prepare_network(None, self.boundary)

    def test_raster_to_points(self):
        self.set_up()
        value = ((population.raster_to_points(self.raster))["geometry"].type == "Point").all()
        expected_value = True
        self.assertTrue(value == expected_value)

    def test_get_network(self):
        # graph from bounding box
        _ = ox.utils_geo.bbox_from_point(location_point, project_utm=True, return_crs=True)
        north, south, east, west = ox.utils_geo.bbox_from_point(location_point, dist=500)
        G = ox.graph_from_bbox(north, south, east, west, network_type="walk")

if __name__ == '__main__':
    unittest.main()
