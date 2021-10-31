import os
import sys
import json
import helper
import pandas as pd
import geopandas as gpd
from configuration import PROJECT_PATH

# map configurations
# path 
DATA_PATH = os.path.join(PROJECT_PATH, "database/data")

# set map configurations functions
def set_mapConfig(field_temp_path, field_map_path, to_js=False):
    # data
    bounds_file = os.path.join(field_temp_path, "field_data.geojson")
    bounds = gpd.read_file(bounds_file)
    print(bounds)

    # center
    field_centroids = bounds.geometry.centroid
    print(field_centroids)
    # center_lat = float(field_centroids.values.y)
    # center_lon = float(field_centroids.values.x)
    # center = dict()
    # center["lat"], center["lon"] = center_lat, center_lon
    # print(center)

    # # scale

    # # map config
    # map_config = dict()
    # map_config["center"] = center
    # map_config["zoom_level"] = 16 #to automate
    # map_config["zoom_controller"] = "topleft"


    # # save map config
    # map_config_file = os.path.join(field_map_path, "map_config.json")
    # with open(map_config_file, 'w') as fp:
    #     json.dump(map_config, fp)

    # # transform to js
    # if to_js :
    #     js_path = helper.transform_geojson_to_js(map_config_file,"var map_config = ")

# geodata directories
geodata_dirs = os.listdir(DATA_PATH)

# remove ".DS_strore" 
if ".DS_Store" in geodata_dirs :
    geodata_dirs.remove(".DS_Store")

geodata_dirs = ["totokro", "polygo_bohoussou_kouame_celestin"]
print(geodata_dirs)

for geodata_dir in geodata_dirs : 
    geodata_abs_dir = os.path.join(DATA_PATH, geodata_dir)
    list_dir = os.listdir(geodata_abs_dir)

    # remove ".DS_strore" 
    if ".DS_Store" in list_dir :
        list_dir.remove(".DS_Store")
    number_fields = len(list_dir)

    # print
    print("\n")
    print(f"number of fields : {number_fields}")
    print(f"existing sub-directories : {list_dir}")

    # get field raw & temp
    for idx in range(number_fields) : 
        raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_dir, idx)
        print("\n...")
        print(raw)

        # set map config json 
        set_mapConfig(temp, map_p, to_js=False)