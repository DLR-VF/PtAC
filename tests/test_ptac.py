"""
Unit tests for PtAC library
"""

import pathlib
import sys
import unittest
import time
import geopandas as gpd

import ptac.accessibility as accessibility
import ptac.population as population
import ptac.util as util


class PtACTest(unittest.TestCase):
    def set_up(self):
        self.data_path = str(pathlib.Path(__file__).parent.absolute())
        self.pt = gpd.read_file(self.data_path + "/input_data/pt_test.gpkg")
        self.pt_low = gpd.read_file(self.data_path + "/input_data/pt_low_test.gpkg")
        self.pt_high = gpd.read_file(self.data_path + "/input_data/pt_high_test.gpkg")
        self.pop = gpd.read_file(self.data_path + "/input_data/pop_test.gpkg")
        self.net = gpd.read_file(self.data_path + "/input_data/net_test.gpkg")
        self.boundary = gpd.read_file(self.data_path + "/input_data/pop_test.gpkg")
        self.raster = self.data_path + "/input_data/raster_test.tif"
        self.timestamp = int(round(time.time()))

    def test_prepare_network(self):
        self.set_up()
        df_prepare_network = accessibility.prepare_network(
            timestamp=self.timestamp, network_gdf=self.net, boundary=self.boundary
        )
        value = df_prepare_network["index"].count()
        self.assertEqual(value, 50)

    def test_network_colums(self):
        # test if network dataset contains necessary columns
        self.set_up()
        df_prepare_network = accessibility.prepare_network(
            timestamp=self.timestamp, network_gdf=self.net, boundary=self.boundary
        )
        diff_columns = len(
            list(
                set(
                    [
                        "index",
                        "fromnode",
                        "tonode",
                        "mode_walk",
                        "mode_bike",
                        "mode_mit",
                        "vmax",
                        "length",
                    ]
                )
                - set(df_prepare_network.columns)
            )
        )
        accessibility.clear_directory()
        self.assertEqual(diff_columns, 0)


    def test_dist_to_closest_max_dist(self):
        self.set_up()
        df_accessibility = accessibility.distance_to_closest(
            self.pop,
            self.pt,
            network_gdf=self.net,
            maximum_distance=50,
        )
        value = df_accessibility["pop"].sum()

        if sys.platform.startswith("win"):
            self.assertAlmostEqual(round(value), 199, delta=1)
        elif sys.platform.startswith("linux"):
            self.assertEqual(round(value), 199)
        elif sys.platform.startswith("macos"):
            self.assertEqual(round(value), 199)

    def test_dist_to_closest_transport_system_low(self):
        self.set_up()
        df_accessibility = accessibility.distance_to_closest(
            self.pop, self.pt_low, network_gdf=self.net, transport_system="low-capacity"
        )
        value = df_accessibility["pop"].sum()

        if sys.platform.startswith("win"):
            self.assertAlmostEqual(round(value), 217, delta=1)
        elif sys.platform.startswith("linux"):
            self.assertEqual(round(value), 217)
        elif sys.platform.startswith("macos"):
            self.assertEqual(round(value), 217)

    def test_dist_to_closest_transport_system_high(self):
        self.set_up()
        df_accessibility = accessibility.distance_to_closest(
            self.pop,
            self.pt_high,
            network_gdf=self.net,
            transport_system="high-capacity",
        )
        value = df_accessibility["pop"].sum()

        if sys.platform.startswith("win"):
            self.assertAlmostEqual(round(value), 217, delta=1)
        elif sys.platform.startswith("linux"):
            self.assertEqual(round(value), 217)
        elif sys.platform.startswith("macos"):
            self.assertEqual(round(value), 218)

    def test_calculate_sdg(self):
        # todo: why it is not 100%?
        self.set_up()
        df_accessibility_low = accessibility.distance_to_closest(
            self.pop, self.pt_low, network_gdf=self.net, transport_system="low-capacity"
        )
        df_accessibility_high = accessibility.distance_to_closest(
            self.pop,
            self.pt_high,
            network_gdf=self.net,
            transport_system="high-capacity",
        )
        value = self.pop
        result = accessibility.calculate_sdg(
            value,
            [df_accessibility_low, df_accessibility_high],
            population_column="pop",
        )
        if sys.platform.startswith("win"):
            self.assertAlmostEqual(round(result, 2), 0.96,  delta=0.01)
            #self.assertEqual(round(result, 2), 0.96)  # 0.9561
        elif sys.platform.startswith("linux"):
            self.assertEqual(round(result, 2), 0.96)
        elif sys.platform.startswith("macos"):
            self.assertEqual(round(result, 2), 0.96)

    def test_raster_to_points(self):
        self.set_up()
        # value = ((population.raster_to_points(self.raster))["geometry"].type == "Point")
        value = population.raster_to_points(self.raster)
        value = float(value["pop"].sum())
        self.assertEqual(round(value), 227)

    def test_project_gdf(self):
        self.set_up()
        value = util.project_gdf(
            gdf=self.pop, geom_col="geometry", to_crs=None, to_latlong=False
        ).crs
        self.assertEqual(value, "epsg:32633")


if __name__ == "__main__":
    unittest.main()
