import unittest
import geopandas
import ptac.accessibility as accessibility
import pathlib


class PtACTest(unittest.TestCase):
    #f data is not None:
    def set_up(self):
        self.data_path = str(pathlib.Path(__file__).parent.absolute())
        self.pt = geopandas.read_file(self.data_path+"/data/pt_example.gpkg")
        self.pop = geopandas.read_file(self.data_path+"/data/population_example.gpkg")
        self.net = geopandas.read_file(self.data_path + "/data/net_example.gpkg")

    def test_dist_to_closest_max_dist(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop, self.pt, network_gdf=self.net,
                                                  maximum_distance=500)["pop"].sum()
        expected_value = 84726.2846339941
        self.assertTrue(value == expected_value)

    def test_dist_to_closest_transport_system(self):
        self.set_up()
        value = accessibility.distance_to_closest(self.pop, self.pt, network_gdf=self.net,
                                                  transport_system="low-capacity")["pop"].sum()
        expected_value = 84726.2846339941
        self.assertTrue(value == expected_value)




if __name__ == '__main__':
    unittest.main()
