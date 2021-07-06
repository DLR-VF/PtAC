import osmnx as ox
import pandas as pd
import timeit


def stats_to_df(stats, row):
    """Converts osmnx Basic_stats dictionary to pd.DataFrame

        Parameters
        -----------
        stats: dictionary
            basic statistics from osmnx

        Returns
        -------
        df : pandas.DataFrame
            statistics as dataframe

       """

    basic_stats = {"zone_id": [int(row["zone_id"])]}
    for key, value in stats.items():
        if isinstance(value, dict):
            for item_key, item_value in value.items():
                basic_stats["{key}_{item_key}".format(key=key, item_key=item_key)] = [item_value]
        else:
            basic_stats[key] = [value]
    df = pd.DataFrame.from_dict(basic_stats)
    return df


def stats(dest_area, crs=None, verbose=0):
    """Calculates network statistics per area

    Parameters
    -----------
    dest_area: geopandas.GeoDataFrame::POLYGON
        Focus area in which to calculate the network statistics

    Returns
    -------
    network_stats : geopandas.GeoDataFrame::POLYGON
        Focus area with network statistics

   """
    start = timeit.default_timer()
    if verbose > 0:
        print(
            "generating network statistics for {number_of_zones} zones\n".format(number_of_zones=len(dest_area.index)))

    if not dest_area.crs == "epsg:4326":
        dest_area = dest_area.to_crs(epsg=4326)

    dest_area_utm = dest_area.to_crs(crs)

    if 'zone_id' not in dest_area.columns:
        dest_area.loc[:, 'zone_id'] = dest_area.index

    network_stats = pd.DataFrame()
    for index, row in dest_area.iterrows():
        bounds = dest_area.iloc[[index]].total_bounds
        G = ox.graph_from_bbox(north=bounds[3], south=bounds[1], east=bounds[2], west=bounds[0])
        G = ox.project_graph(G, crs)
        stats = ox.basic_stats(G, area=dest_area_utm.iloc[[index]].unary_union.area)
        if verbose > 0:
            print("stats for zone_id {zone_id}: {stats}\n".format(zone_id=row["zone_id"], stats=stats))
        stats_df = stats_to_df(stats, row)
        network_stats = pd.concat([network_stats, stats_df], axis=0, ignore_index=True)

    network_stats.fillna(0, inplace=True)
    network_stats = dest_area[["zone_id", "geometry"]].merge(network_stats, how="left", left_on="zone_id",
                                                             right_on="zone_id")
    stop = timeit.default_timer()
    if verbose > 0:
        print("network statistics calculated in {exec_time} seconds".format(exec_time=stop - start))
    return network_stats
