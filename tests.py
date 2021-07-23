import unittest
import geopandas
import ptac.accessibility as accessibility
import pathlib

# inheriting from unittest.TestCase gives access to a lot of different testing capabilities within the class
class PtACTest(unittest.TestCase):
    #f data is not None:
    def set_up(self):
        self.data_path = str(pathlib.Path(__file__).parent.absolute())
        self.pt = geopandas.read_file(self.data_path+"/data/pt_example.gpkg")
        self.pt_low = geopandas.read_file(self.data_path+"/data/pt_low_example.gpkg")
        self.pt_high = geopandas.read_file(self.data_path+"/data/pt_high_example.gpkg")
        self.pop = geopandas.read_file(self.data_path+"/data/population_example.gpkg")
        self.net = geopandas.read_file(self.data_path + "/data/net_example.gpkg")

    def test_dist_to_closest_max_dist(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop,
                                                  self.pt,
                                                  network_gdf=self.net,
                                                  maximum_distance=500)["pop"].sum()
        expected_value = 84743.88444411755
        self.assertTrue(value == expected_value)

    def test_dist_to_closest_transport_system(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop, self.pt_low, network_gdf=self.net,
                                                  transport_system="low-capacity")["pop"].sum()
        expected_value = 67550.55961567163 # 84726.2846339941
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
        expected_result = 0.9855756017281202
        self.assertTrue(result == expected_result)

if __name__ == '__main__':
    unittest.main()
