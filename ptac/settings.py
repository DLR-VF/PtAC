#!/usr/bin/env python3
# coding:utf-8

"""Defines street types"""

"""
@name : settings.py
@author : Simon Nieland, Serra Yosmaoglu
@date : 26.07.2021
@copyright : Institut fuer Verkehrsforschung, Deutsches Zentrum fuer Luft- und Raumfahrt
"""

import pandas as pd

default_crs = "epsg:4326"


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

    "raceway": [False, False, False, 160, 1],
    "ford": [False, False, False, 10, 1],

    "railway_rail": [False, False, False, 300, 1],
    "railway_tram": [False, False, False, 100, 1],
    "railway_light_rail": [False, False, False, 100, 1],
    "railway_subway": [False, False, False, 100, 1],
    "railway_preserved": [False, False, False, 100, 1]
        },      orient="index", columns=['mode_walk', 'mode_bike', 'mode_mit', 'vmax', 'lanes'])\
    #.reset_index(inplace=True)\
    #.rename(columns={"index": "street_type"}, inplace=True)

