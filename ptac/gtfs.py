#partly adapted from partridge (https://github.com/remix/partridge)
import pandas as pd
import os
import numpy as np
import geopandas as gpd
import sys
from shapely.geometry import Point, LineString
import datetime
from collections import defaultdict
from datetime import datetime
import ptac.settings as settings


DATE_FORMAT = "%Y%m%d"

DAY_NAMES = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def parse_date(val: str) -> datetime.date:
    """

    :param val: 
    :return: 
    """
    return datetime.datetime.strptime(val, DATE_FORMAT).date()


def parse_time(val: str) -> np.float64:
    """
    :param val:
    :return: 
    """
    if val is np.nan:
        return val

    val = val.strip()

    if val == "":
        return np.nan

    h, m, s = val.split(":")
    ssm = int(h) * 3600 + int(m) * 60 + int(s)

    # pandas doesn't have a NaN int, use floats
    return np.float64(ssm)


def empty_df(columns=None) -> pd.DataFrame:
    """

    :param columns:
    :return:
    """
    # todo: docstrings
    columns = [] if columns is None else columns
    empty = {col: [] for col in columns}
    return pd.DataFrame(empty, columns=columns, dtype=np.unicode)


class GtfsTable(object):
    # todo: docstrings
    def __init__(self, table_name):
        self._name = table_name
        self.required_columns = ()
        self.get_required_columns(table_name)
        self.df = pd.DataFrame()
        #self.conn

    def get_required_columns(self, table_name):
        """
        checks if all required columns are in the gtfs tables. if not, required columns are added and left empty
        :param table_name: name of the db table
        :rtype table_name: String


        :rtype: object
        """
        # todo: docstrings

        if table_name == "routes.txt":
            self.required_columns = {
                "route_id": "",
                "route_short_name": "",
                "route_long_name": "",
                "route_type": "numeric",
            }

        if table_name == "stops.txt":
            self.required_columns = {
                "stop_id": "",
                "stop_name": "",
                "stop_lat": "numeric",
                "stop_lon": "numeric", #todo: add pos column
            }

        if table_name == "stop_times.txt":
            self.required_columns = {
                                        "trip_id": "",
                                        "arrival_time": "time",
                                        "departure_time": "time",
                                        "stop_id": "",
                                        "stop_sequence": "numeric",
            }

        if table_name == "trips.txt":
            self.required_columns = {"route_id": "", "service_id": "", "trip_id": ""}

    def add_required_columns(self, df):
        """

        :param df:
        """
        # todo: docstrings
        missing_columns = list(set(self.required_columns).difference(set(df.columns.values)))
        for column in missing_columns:
            print("Column {column} in table {table} is missing. Adding an empty column. "
                  "This will probably lead to problems..".format(column=column,
                                                                 table=self._name))
            df[column] = pd.Series(dtype=int)
        self.df = df


class Feed(object):
    def __init__(self, path):
        self.root_path = path
        self.routes = self._read_file("routes.txt")
        self.stops = self._read_file("stops.txt")
        self._stops_to_gdf()
        self.stop_times = self._read_file("stop_times.txt")
        self.trips = self._read_file("trips.txt")
        self.departures_per_stop = self.get_departures_per_stop()

    def _stops_to_gdf(self, crs=settings.default_crs):
        """

        :param crs:
        """
        # todo: docstrings
        if self.stops.empty:
            self.stops = gpd.GeoDataFrame(self.stops, geometry=[], crs=crs)

        self.stops["geometry"] = self.stops.apply(lambda s: Point(s.stop_lon, s.stop_lat), axis=1)

        self.stops.drop(["stop_lon", "stop_lat"], axis=1, inplace=True)
        self.stops = gpd.GeoDataFrame(self.stops, crs=crs)


    def _read_file(self, file_name):
        """

        :param file_name:
        :return:
        """
        # todo: docstrings
        _file = "{root_path}/{file_name}".format(root_path=self.root_path,
                                                 file_name=file_name)
        gtfs_table = GtfsTable(file_name)

        if not os.path.exists(_file):
            # The file is missing or empty. Return an empty
            # DataFrame containing any required columns.
            df = empty_df(gtfs_table.required_columns.keys())

        else:
            df = pd.read_csv(_file)

        for column in list(gtfs_table.required_columns.keys()):
            if gtfs_table.required_columns[column] == "numeric":
                df[column] = pd.to_numeric(df[column])
            if gtfs_table.required_columns[column] == "date":
                df[column] = pd.to_datetime(df[column], format="%Y%m%d", errors='ignore')
            if gtfs_table.required_columns[column] == "time":
                df[column] = pd.to_datetime(df[column], format="%H%M%S", errors='ignore')
            #patch
            if gtfs_table.required_columns[column] == "string":
                df[column] = df[column].astype(str)

        gtfs_table.add_required_columns(df)
        return gtfs_table.df

    def get_departures_per_stop(self, date="20180912", old_route_type_def=True):
        """

        :param area_gdf:
        :param date:
        :param old_route_type_def:
        :return:
        """
        #todo: docstrings
        #if 'zone_id' not in area_gdf.columns:
        #    area_gdf.loc[:, 'zone_id'] = area_gdf.index

        #area_gdf_buffered = area_gdf.copy()
        #area_gdf_buffered["geometry"] = area_gdf.buffer(200)

        #dateobj = datetime.strptime(date, DATE_FORMAT).date()
        #day_of_week = dateobj.strftime('%A').lower()

        #calendar = self.calendar[self.calendar[day_of_week]==1]
        #print(self.calendar_dates["date"].dt.date)

        # calendar_dates = self.calendar_dates[self.calendar_dates["date"].dt.date==dateobj]
        # select only trips with relevant service_id
        if old_route_type_def:
            route_types = settings.old_route_types
        else:
            route_types = settings.new_route_types

        #trips = self.trips[self.trips.service_id == calendar.service_id.iloc[0]]
        count = self.stop_times.groupby(["stop_id"])
        trips = self.trips.merge(self.routes, how="left", on="route_id")
        stop_times = self.stop_times.merge(trips, how="left", on="trip_id")
        stop_times["bus"] = 0
        stop_times.loc[stop_times["route_type"] == route_types["bus"],  "bus"] = 1

        stop_times["tram"] = 0
        stop_times.loc[stop_times["route_type"] == route_types["tram"],  "tram"] = 1

        stop_times["rail"] = 0
        stop_times.loc[stop_times["route_type"] == route_types["rail"], "rail"] = 1

        stop_times["subway"] = 0
        stop_times.loc[stop_times["route_type"] == route_types["subway"], "subway"] = 1

        stop_times["ferry"] = 0
        stop_times.loc[stop_times["route_type"] == route_types["ferry"], "ferry"] = 1

        departures = stop_times.groupby(['stop_id'])["bus", "tram", "rail", "subway", "ferry"].agg('sum')
        departures = departures.reset_index().rename(columns={'index': 'stop_id'})

        return self.stops.merge(departures, how="right", on="stop_id")
