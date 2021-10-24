import os
import sys
import json
import helper
import pandas as pd
import geopandas as gpd

# map configurations
# path 
PROJ_ABS_PATH = os.path.dirname(os.getcwd())
DATA_ABS_PATH = os.path.join(PROJ_ABS_PATH, "database/data")
sys.path.append(DATA_ABS_PATH)

# data
bounds_file = os.path.join(DATA_ABS_PATH, "temp/field_data.geojson")
bounds = gpd.read_file(bounds_file)

# center
field_centroids = bounds.geometry.centroid
center_lat = float(field_centroids.values.y)
center_lon = float(field_centroids.values.x)
center = dict()
center["lat"], center["lon"] = center_lat, center_lon
print(center)

# scale

# map config
map_config = dict()
map_config["center"] = center
map_config["zoom_level"] = 16 #to automate
map_config["zoom_controller"] = "topleft"


# save map config
map_config_file = os.path.join(DATA_ABS_PATH, "map/map_config.json")
with open(map_config_file, 'w') as fp:
    json.dump(map_config, fp)

# transform to js
js_path = helper.transform_geojson_to_js(map_config_file,"var map_config = ")
