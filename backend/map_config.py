import os
import sys
import json
import pandas as pd
import geopandas as gpd
from IPython.display import display

# map configurations
# data path 
DATA_REL_PATH = "./../../database/data"
sys.path.append("DATA_REL_PATH")

# data
bounds_file = os.path.join(DATA_REL_PATH, "temp/field_data.geojson")
bounds = gpd.read_file(bounds_file)

# center
field_centroids = bounds.geometry.centroid
center_lat = float(field_centroids.values.y)
center_lon = float(field_centroids.values.x)
center = dict()
center["lat"], center["lon"] = center_lat, center_lon
display(center)

# scale

# map config
map_config = dict()
map_config["center"] = center


# save map config
map_config_file = os.path.join(DATA_REL_PATH, "map/map_config.json")
with open(map_config_file, 'w') as fp:
    json.dump(map_config, fp)
