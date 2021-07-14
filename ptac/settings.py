import pandas as pd

default_crs = "epsg:4326"

osm_restaurants_tags = {"amenity": ['restaurant', 'fast_food', 'food_court', 'cafe', 'ice_cream']}
osm_parks_tags = {"leisure": ['park', 'garden', 'nature_reserve'], "landuse": ["forest", "village_green", "recreation_ground"]}



#mode, mode_walk, mode_bike, mode_mit, vmax, lanes
highways = pd.DataFrame.from_dict({
    "highway_motorway": [False, False, True,  160, 2],
    "highway_motorway_link": [False, False, True, 80, 1],
    "highway_trunk": [True, True, True, 100, 2],
    "highway_trunk_link": [True, True, True, 80, 1],
    "highway_primary": [True, True, True, 100, 2],
    "highway_primary_link": [True, True, True, 80, 1],
    "highway_secondary": [True, True, True, 100, 2],
    "highway_secondary_link": [True, True, True, 80, 1],
    "highway_tertiary": [True, True, True, 80, 1],
    "highway_tertiary_link": [True, True, True, 80, 1],
    "highway_unclassified": [True, True, True, 80, 1],
    "highway_residential": [True, True, True, 50, 1],
    "highway_living_street": [True, True, True, 10, 1],
    "highway_road": [True, True, True, 30, 1],

    "highway_service": [True, True, False, 20, 1],
    "highway_track": [True, True, True, 20, 1],
    # True, True, True only if destination (http://wiki.openstreetmap.org/wiki/OSM_tags_for_routing/Access-Restrictions#Germany)
    "highway_services": [True, True, True, 30, 1],
    "highway_unsurfaced": [True, True, True, 30, 1],

    # TODO: we should decide which of the following ones may be used by which mode
    "highway_path": [True, True, False, 10, 1],
    "highway_bridleway": [False, False, False, 10, 1],
    "highway_cycleway": [False, True, False, 10, 1],
    "highway_pedestrian": [True, False, False, 10, 1],
    "highway_footway": [True, True, False, 10, 1],
    "highway_step": [True, True, False, 10, 1],
    "highway_steps": [True, True, False, 10, 1],
    "highway_stairs": [True, True, False, 10, 1],
    "highway_bus_guideway": [False, True, False, 50, 1],
    #
    "highway_raceway": [False, False, False, 160, 1],
    "highway_ford": [False, False, False, 10, 1],

    "railway_rail": [False, False, False, 300, 1],
    "railway_tram": [False, False, False, 100, 1],
    "railway_light_rail": [False, False, False, 100, 1],
    "railway_subway": [False, False, False, 100, 1],
    "railway_preserved": [False, False, False, 100, 1],
  
    #"highway_corridor": [True, True, False, 20, 1],
    #"highway_elevator": [True, False, False, 10, 1],
    #"highway_rest_area": [True, True, False, 20, 1]
}, orient="index", columns=['mode_walk', 'mode_bike', 'mode_mit', 'vmax', 'lanes'])

old_route_types = {
    "bus" : 3,
    "tram": 0,
    "rail": 2,
    "subway": 1,
    "ferry": 4,
}

#todo: properly include new route types
new_route_types = {
    "bus" : 700,
    "tram": 900,
    "rail": 100,
    "subway": [400, 401],
    "ferry": 1000,
    "aerialway": [1300, 1301],
    "suburban": 109,
    "ic": 2
}

# Street types without highway initialization
#mode, mode_walk, mode_bike, mode_mit, vmax, lanes
streettypes = pd.DataFrame.from_dict({
    "motorway": [False, False, True,  160, 2],
    "motorway_link": [False, False, True, 80, 1],
    "trunk": [True, True, True, 100, 2],
    "trunk_link": [True, True, True, 80, 1],
    "primary": [True, True, True, 100, 2],
    "primary_link": [True, True, True, 80, 1],
    "secondary": [True, True, True, 100, 2],
    "secondary_link": [True, True, True, 80, 1],
    "tertiary": [True, True, True, 80, 1],
    "tertiary_link": [True, True, True, 80, 1],
    "unclassified": [True, True, True, 80, 1],
    "residential": [True, True, True, 50, 1],
    "living_street": [True, True, True, 10, 1],
    "road": [True, True, True, 30, 1],
    "service": [True, True, False, 20, 1],
    "track": [True, True, True, 20, 1],
    # True, True, True only if destination (http://wiki.openstreetmap.org/wiki/OSM_tags_for_routing/Access-Restrictions#Germany)
    "services": [True, True, True, 30, 1],
    "unsurfaced": [True, True, True, 30, 1],

    # TODO: we should decide which of the following ones may be used by which mode
    "path": [True, True, False, 10, 1],
    "bridleway": [False, False, False, 10, 1],
    "cycleway": [False, True, False, 10, 1],
    "pedestrian": [True, False, False, 10, 1],
    "footway": [True, True, False, 10, 1],
    "step": [True, True, False, 10, 1],
    "steps": [True, True, False, 10, 1],
    "stairs": [True, True, False, 10, 1],
    "bus_guideway": [False, True, False, 50, 1],

    #
    "raceway": [False, False, False, 160, 1],
    "ford": [False, False, False, 10, 1],

    "railway_rail": [False, False, False, 300, 1],
    "railway_tram": [False, False, False, 100, 1],
    "railway_light_rail": [False, False, False, 100, 1],
    "railway_subway": [False, False, False, 100, 1],
    "railway_preserved": [False, False, False, 100, 1]
}, orient="index", columns=['mode_walk', 'mode_bike', 'mode_mit', 'vmax', 'lanes'])

