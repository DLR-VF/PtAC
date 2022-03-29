"""
Unit tests for PtAC library
"""


import unittest
import geopandas
import ptac.accessibility as accessibility
import ptac.population_new as population_new
import pathlib


# inheriting from unittest. TestCase gives access to a lot of different testing capabilities within the class
class PtACTest(unittest.TestCase):

    #f data is not None:

    def set_up(self):
        self.data_path = str(pathlib.Path(__file__).parent.absolute())
        self.pt = geopandas.read_file(self.data_path+"/input_data/pt_example.gpkg")
        self.pt_low = geopandas.read_file(self.data_path+"/input_data/pt_low_example.gpkg")
        self.pt_high = geopandas.read_file(self.data_path+"/input_data/pt_high_example.gpkg")
        self.pop = geopandas.read_file(self.data_path+"/input_data/population_example.gpkg")
        self.net = geopandas.read_file(self.data_path + "/input_data/net_example.gpkg")
        self.boundary = geopandas.read_file(self.data_path + "/input_data/boundary_example.gpkg")
        self.raster = self.data_path + "/input_data/friedrichshain_raster.tif"


    def test_dist_to_closest_max_dist(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop,
                                                  self.pt,
                                                  network_gdf=self.net,
                                                  maximum_distance=500)["pop"].sum()
        expected_value = 84743.98387801647
        self.assertTrue(value == expected_value)


    def test_dist_to_closest_transport_system(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop,
                                                  self.pt_low,
                                                  network_gdf=self.net,
                                                  transport_system="low-capacity")["pop"].sum()
        expected_value = 67550.65904957056
        self.assertTrue(value == expected_value)


    def test_calculate_sdg(self):
        self.set_up()
    #     value_access = accessibility.distance_to_closest(self.pop,
    #                                               self.pt,
    #                                               network_gdf=self.net,
    #                                               maximum_distance=500)
    #     value = self.pop
    #     result = accessibility.calculate_sdg(value, value_access, population_column="pop")
    #     expected_result = 0.9600453741136
    #     self.assertTrue(result == expected_result)

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
        self.assertTrue(result == expected_result)


    def test_raster_to_points(self):
        self.set_up()
        value = ((population_new.raster_to_points(self.raster))["geometry"].type == "Point").all()
        expected_value = True
        self.assertTrue(value == expected_value)


if __name__ == '__main__':
    unittest.main()
