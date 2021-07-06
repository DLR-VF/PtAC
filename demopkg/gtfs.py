#partly adapted from partridge (https://github.com/remix/partridge)
import pandas as pd
import os
import numpy as np
import geopandas as gpd
import sys
from shapely.geometry import Point, LineString
import demopkg.urbanspatialio as io
import datetime
from collections import defaultdict
from datetime import datetime
from sqlalchemy import create_engine
import demopkg.settings as settings

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
        if table_name == "agency.txt":
            self.required_columns = {"agency_name":"", "agency_url": "", "agency_timezone":""}
            #  	cursor.execute("""CREATE TABLE public.%s_agency ( agency_id varchar(8),agency_name text,agency_url text,agency_timezone varchar(40),agency_lang varchar(2),agency_phone varchar(20) );""" % dbName)
        if table_name == "calendar.txt":
            self.required_columns = {"service_id": "",
                                     "monday": "numeric",
                                     "tuesday": "numeric",
                                     "wednesday": "numeric",
                                     "thursday": "numeric",
                                     "friday": "numeric",
                                     "saturday": "numeric",
                                     "sunday": "numeric",
                                     "start_date": "date", #todo: change for urmoac compatibility
                                     "end_date": "date", #todo: change for urmac compatibility
            }
            # 99 	cursor.execute("""CREATE TABLE public.%s_calendar ( service_id varchar(8),monday smallint,tuesday smallint,wednesday smallint,thursday smallint,friday smallint,saturday smallint,sunday smallint,start_date integer,end_date integer );""" % dbName)

        if table_name == "calendar_dates.txt":
            self.required_columns = ({"service_id": "",
                                      "date": "date",
                                      "exception_type": "numeric"})
        # 100 	cursor.execute("""CREATE TABLE public.%s_calendar_dates ( service_id varchar(8),date integer,exception_type smallint );""" % dbName)
        if table_name == "fare_attributes.txt":
            self.required_columns = {
                "fare_id": "",
                "price": "numeric",
                "currency_type": "",
                "payment_method": "",
                "transfers": "",
            }

        if table_name == "fare_rules.txt":
            self.required_columns = {"fare_id": "",}
            
        if table_name == "feed_info.txt":
            self.required_columns = {"feed_publisher_name": "",
                                     "feed_publisher_url": "",
                                     "feed_lang": ""}

        if table_name == "frequencies.txt":
            self.required_columns = {
                "trip_id": "",
                "start_time": "time",
                "end_time": "time",
                "headway_secs": "numeric",
            }

        if table_name == "routes.txt":
            self.required_columns = {
                "route_id": "",
                "route_short_name": "",
                "route_long_name": "",
                "route_type": "numeric",
            }
        # 101 	cursor.execute("""CREATE TABLE public.%s_routes ( route_id varchar(8),agency_id varchar(8), route_short_name varchar(8),route_long_name varchar(80),route_desc text,route_type smallint,route_url varchar(40),route_color varchar(6),route_text_color varchar(20) );""" % dbName)

        if table_name == "shapes.txt":
            self.required_columns = {
                "shape_id": "",
                "shape_pt_lat": "numeric",
                "shape_pt_lon": "numeric",
                "shape_pt_sequence": "numeric",
            }

        if table_name == "stops.txt":
            self.required_columns = {
                "stop_id": "",
                "stop_name": "",
                "stop_lat": "numeric",
                "stop_lon": "numeric", #todo: add pos column
            }
            # 103 	cursor.execute("""CREATE TABLE public.%s_stops ( stop_id varchar(8),stop_code varchar(40),stop_name varchar(80),stop_desc text,stop_lat real,stop_lon real,zone_id varchar(8),stop_url varchar(40),location_type smallint,parent_station varchar(8));""" % dbName)

        if table_name == "stop_times.txt":
            self.required_columns = {
                                        "trip_id": "",
                                        "arrival_time": "time",
                                        "departure_time": "time",
                                        "stop_id": "",
                                        "stop_sequence": "numeric",
            }
            # 102 	cursor.execute("""CREATE TABLE public.%s_stop_times ( trip_id integer,arrival_time integer,departure_time integer,stop_id varchar(8),stop_sequence smallint,stop_headsign varchar(40),pickup_type smallint,drop_off_type smallint,shape_dist_traveled text);""" % dbName)

        if table_name == "transfers.txt":
            self.required_columns = {"from_stop_id": "",
                                     "to_stop_id": "",
                                     "from_trip_id": "string",
                                     "to_trip_id": "string",
                                     "transfer_type": "numeric"}
        # 104 	cursor.execute("""CREATE TABLE public.%s_transfers ( from_stop_id varchar(8),to_stop_id varchar(8),transfer_type smallint,min_transfer_time real,from_trip_id varchar(8),to_trip_id varchar(8) );""" % dbName)

        if table_name == "trips.txt":
            self.required_columns = {"route_id": "", "service_id": "", "trip_id": ""}

        # 105 	cursor.execute("""CREATE TABLE public.%s_trips ( route_id varchar(8),service_id varchar(8),trip_id integer,trip_headsign varchar(80),trip_short_name varchar(8),direction_id varchar(8),block_id varchar(8),shape_id varchar(8) );""" % dbName)

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
        self.agency = self._read_file("agency.txt")
        self.calendar = self._read_file("calendar.txt")
        self.calendar_dates = self._read_file("calendar_dates.txt")
        self.fare_attributes = self._read_file("fare_attributes.txt")
        self.fare_rules = self._read_file("fare_rules.txt")
        self.feed_info = self._read_file("feed_info.txt")
        self.frequencies = self._read_file("frequencies.txt")
        self.routes = self._read_file("routes.txt")
        self.shapes = self._read_file("shapes.txt")
        self.shapes_to_gdf()
        self.stops = self._read_file("stops.txt")
        self._stops_to_gdf()
        self.stop_times = self._read_file("stop_times.txt")
        self.transfers = self._read_file("transfers.txt")
        self.trips = self._read_file("trips.txt")

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

    def shapes_to_gdf(self, crs=settings.default_crs):
        """

        :param crs:
        """
        # todo: docstrings
        if self.shapes.empty:
            self.shapes = gpd.GeoDataFrame({"shape_id": [], "geometry": []}, crs=crs)

        data = {"shape_id": [], "geometry": []}
        for shape_id, shape in self.shapes.sort_values("shape_pt_sequence").groupby("shape_id"):
            data["shape_id"].append(shape_id)
            data["geometry"].append(
                LineString(list(zip(shape.shape_pt_lon, shape.shape_pt_lat)))
            )
        self.shapes = gpd.GeoDataFrame(data, crs=crs)

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
                #df[column] = df.apply(lambda row: parse_time(str(row[column])), axis=1)
                #df[column] = pd.to_numeric(df[column])

        gtfs_table.add_required_columns(df)
        return gtfs_table.df

    def _service_ids_by_date(self):# -> Dict[datetime.date, FrozenSet[str]]:
        """

        :return:
        """
        # todo: docstrings
        # todo: remove?
        results = defaultdict(set)# DefaultDict[datetime.date, Set[str]] = defaultdict(set)
        removals = defaultdict(set)#  DefaultDict[datetime.date, Set[str]] = defaultdict(set)

        service_ids = set(self.trips.service_id)
        calendar = self.calendar
        caldates = self.calendar_dates

        if not calendar.empty:
            # Only consider calendar.txt rows with applicable trips
            calendar = calendar[calendar.service_id.isin(service_ids)].copy()

        if not caldates.empty:
            # Only consider calendar_dates.txt rows with applicable trips
            caldates = caldates[caldates.service_id.isin(service_ids)].copy()

        if not calendar.empty:
            # Parse dates
            #calendar.start_date = parse_date(calendar.start_date)
            #calendar.end_date = parse_date(calendar.end_date)

            # Build up results dict from calendar ranges
            for _, cal in calendar.iterrows():
                start = cal.start_date.toordinal()
                end = cal.end_date.toordinal()

                dow = {i: cal[day] for i, day in enumerate(DAY_NAMES)}
                for ordinal in range(start, end + 1):
                    date = datetime.date.fromordinal(ordinal)
                    if int(dow[date.weekday()]):
                        results[date].add(cal.service_id)

        if not caldates.empty:
            # Parse dates
            #caldates.date = parse_date(caldates.date)

            # Split out additions and removals
            cdadd = caldates[caldates.exception_type == 1.0]
            cdrem = caldates[caldates.exception_type == 2.0]

            # Add to results by date
            for _, cd in cdadd.iterrows():
                results[cd.date].add(cd.service_id)

            # Collect removals
            for _, cd in cdrem.iterrows():
                removals[cd.date].add(cd.service_id)

            # Finally, process removals by date
            for date in removals:
                for service_id in removals[date]:
                    if service_id in results[date]:
                        results[date].remove(service_id)

                # Drop the key from results if no service present
                if len(results[date]) == 0:
                    del results[date]

        assert results, "No service found in feed."

        return {k: frozenset(v) for k, v in results.items()}

    def _dates_by_service_ids(self): # -> Dict[FrozenSet[str], FrozenSet[datetime.date]]:
        """

        :return:
        """
        # todo: docstrings
        results = defaultdict(set)#: DefaultDict[FrozenSet[str], Set[datetime.date]] = defaultdict(set)
        for date, service_ids in self._service_ids_by_date().items():
            results[service_ids].add(date)
        return {k: frozenset(v) for k, v in results.items()}

    def trip_counts_by_date(self):
        """

        :return:
        """
        # todo: docstrings
        results = defaultdict(int)
        trips = self.trips
        for service_ids, dates in self._dates_by_service_ids().items():
            trip_count = trips[trips.service_id.isin(service_ids)].shape[0]
            for date in dates:
                results[date] += trip_count
        return dict(results)

    def _connect_to_db(self, db_access):
        """

        :param db_access:
        """
        #todo: docstrings
        try:
            engine = create_engine(
                'postgresql://{user_name}:{password}@{host}:5432/{db_name}'.format(user_name=db_access["user_name"],
                                                                                   password=db_access["password"],
                                                                                   host=db_access["host"],
                                                                                   db_name=db_access["db_name"]))
            self.conn = engine.connect()

        except Exception as e:
            print(e)
            sys.exit()

    def number_of_departures_per_area(self, area_gdf, date="20180912", old_route_type_def=False):
        """

        :param area_gdf:
        :param date:
        :param old_route_type_def:
        :return:
        """
        #todo: docstrings
        if 'zone_id' not in area_gdf.columns:
            area_gdf.loc[:, 'zone_id'] = area_gdf.index

        area_gdf_buffered = area_gdf.copy()
        area_gdf_buffered["geometry"] = area_gdf.buffer(200)

        dateobj = datetime.strptime(date, DATE_FORMAT).date()
        day_of_week = dateobj.strftime('%A').lower()

        calendar = self.calendar[self.calendar[day_of_week]==1]
        #print(self.calendar_dates["date"].dt.date)

        # calendar_dates = self.calendar_dates[self.calendar_dates["date"].dt.date==dateobj]
        # select only trips with relevant service_id
        if old_route_type_def:
            route_types = settings.old_route_types
        else:
            route_types = settings.new_route_types

        trips = self.trips[self.trips.service_id == calendar.service_id.iloc[0]]
        trips = trips.merge(self.routes, how="left", on="route_id")
        stop_times = trips.merge(self.stop_times, how="left", on="trip_id")
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
        departures = self.stops.merge(departures, how="right", on="stop_id")
        departures = departures.to_crs(area_gdf_buffered.crs)
        stops_in_zones = gpd.sjoin(area_gdf_buffered,
                                       departures,
                                       how="inner", op='contains')
        departures_in_zones = stops_in_zones.groupby(['zone_id'])["bus", "tram", "rail", "subway", "ferry"].agg('sum').reset_index().rename(columns={'index': 'zone_id'})

        departures_in_zones = area_gdf.merge(departures_in_zones, how="left", left_on="zone_id", right_on="zone_id")
        return departures_in_zones

    def to_db(self, db_access, prefix=""):
        """

        :param db_access:
        :param prefix:
        """
        # todo: docstrings
        self._connect_to_db(db_access=db_access)
        self.agency.to_sql(prefix+"_agency", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.calendar.to_sql(prefix+"_calendar", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.calendar_dates.to_sql(prefix+"_calendar_dates", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.fare_attributes.to_sql(prefix+"_fare_attributes", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.fare_rules.to_sql(prefix+"_fare_rules", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.feed_info.to_sql(prefix+"_feed_info", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.frequencies.to_sql(prefix+"_frequencies", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.routes.to_sql(prefix+"_routes", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        io.to_postgis(self.shapes, self.conn, table_name=prefix+"_shapes", schema=db_access["schema"], if_exists='replace')
        io.to_postgis(self.stops, self.conn, table_name=prefix+"_stops", schema=db_access["schema"], if_exists='replace')
        self.stop_times.to_sql(prefix+"_stop_times", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.transfers.to_sql(prefix+"_transfers", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.trips.to_sql(prefix+"_trips", self.conn, db_access["schema"], if_exists='replace',  method='multi')

    def to_db_urmoac_compatible(self, db_access, prefix="", crs="epsg:32719"):
        """

        :rtype: object
        """
        # todo: docstrings
        self._connect_to_db(db_access=db_access)
        self.agency.to_sql(prefix+"_agency", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.calendar['start_date'] = self.calendar['start_date'].dt.strftime('%Y%m%d').astype(int)
        self.calendar['end_date'] = self.calendar['end_date'].dt.strftime('%Y%m%d').astype(int)
        self.calendar['service_id'] = self.calendar['service_id'].astype(str)
        self.calendar.to_sql(prefix+"_calendar", self.conn, db_access["schema"], if_exists='replace',  method='multi')

        self.calendar_dates['service_id'] = self.calendar_dates['service_id'].astype(str)
        self.calendar_dates['date'] = self.calendar_dates['date'].dt.strftime('%Y%m%d').astype(int)
        self.calendar_dates.to_sql(prefix+"_calendar_dates", self.conn, db_access["schema"], if_exists='replace',  method='multi')

        self.fare_attributes.to_sql(prefix+"_fare_attributes", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.fare_rules.to_sql(prefix+"_fare_rules", self.conn, db_access["schema"], if_exists='replace',  method='multi')
        self.feed_info.to_sql(prefix+"_feed_info", self.conn, db_access["schema"], if_exists='replace',  method='multi')

        self.frequencies['trip_id'] = self.frequencies['trip_id'].astype(str)
        self.frequencies.to_sql(prefix+"_frequencies", self.conn, db_access["schema"], if_exists='replace',  method='multi')

        self.routes["route_id"] = self.routes["route_id"].astype(str)

        self.routes.to_sql(prefix+"_routes", self.conn, db_access["schema"], if_exists='replace',  method='multi')

        self.shapes["shape_id"] = self.shapes["shape_id"].astype(str)
        io.to_postgis(self.shapes.to_crs(crs), self.conn, table_name=prefix+"_shapes", schema=db_access["schema"], if_exists='replace')

        self.stops["stop_id"] = self.stops["stop_id"].astype(str)
        io.to_postgis(self.stops.to_crs(crs), self.conn, table_name=prefix+"_stops", schema=db_access["schema"], if_exists='replace')
        sql_sting = "alter table {schema}.{prefix}_stops rename column geometry to pos;".format(schema=db_access["schema"], prefix=prefix)
        self.conn.execute(sql_sting)

        self.stop_times['trip_id'] = self.stop_times['trip_id'].astype(str)
        self.stop_times['stop_id'] = self.stop_times['stop_id'].astype(str)
        self.stop_times['arrival_time'] = self.stop_times['arrival_time'].astype(str)
        self.stop_times['departure_time'] = self.stop_times['departure_time'].astype(str)

        if not self.transfers.empty:
            self.transfers["to_trip_id"] = self.transfers["to_trip_id"].astype(str)
            self.transfers["from_trip_id"] = self.transfers["from_trip_id"].astype(str)
            self.transfers["to_route_id"] = self.transfers["to_route_id"].astype(str)
            self.transfers["from_route_id"] = self.transfers["from_route_id"].astype(str)
            self.transfers.to_sql(prefix+"_transfers", self.conn, db_access["schema"], if_exists='replace',  method='multi')

        self.trips["trip_id"] = self.trips["trip_id"].astype(str)
        self.trips["route_id"] = self.trips["route_id"].astype(str)
        self.trips["service_id"] = self.trips["service_id"].astype(str)
        self.trips.to_sql(prefix+"_trips", self.conn, db_access["schema"], if_exists='replace',  method='multi')




