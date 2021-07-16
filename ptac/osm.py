import osmnx as ox


def get_facility(polygon, facility):
    return ox.pois_from_polygon(polygon, tags=facility)


def get_landuse(polygon,):
    return ox.footprints_from_polygon(polygon, footprint_type="landuse")


def get_restaurants(polygon):
    return ox.pois_from_polygon(polygon, tags={"amenity": 'restaurant'})


def get_parks(polygon):
    return ox.pois_from_polygon(polygon, tags={"leisure": 'park'})


def get_network(polygon, network_type="walk", custom_filter=None):
    bounds = polygon.bounds
    return ox.graph_from_bbox(north=bounds[3], south=bounds[1], east=bounds[2], west=bounds[0],
                              custom_filter=custom_filter, simplify=False)


def get_buildings(polygon):
    return ox.footprints.footprints_from_polygon(polygon, footprint_type='building', retain_invalid=False)
