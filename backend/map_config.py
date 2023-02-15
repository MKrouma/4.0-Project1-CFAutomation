import os
import sys
import json
import pandas as pd
import geopandas as gpd

from module import helper
from backend.python.settings import PROJECT_PATH

# set map configurations functions
def set_mapConfig(field_temp_path, field_map_path, to_js=False, overwrite=False):
    # data
    bounds_file = os.path.join(field_temp_path, "field_data.geojson")
    bounds = gpd.read_file(bounds_file)
    print(bounds)

    # center
    field_centroids = bounds.geometry.centroid
    print(field_centroids)
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
    map_config_file = os.path.join(field_map_path, "map_config.json")
    if not os.path.exists(map_config_file) or overwrite==True:
        with open(map_config_file, 'w') as fp:
            json.dump(map_config, fp)
        print(f"{map_config_file} created !")
    else :
        print(f"{map_config_file} exists !") 

    # transform to js
    if to_js :
        js_path = helper.transform_geojson_to_js(map_config_file,"var map_config = ")


if __name__ == "__main__" :
    # map configurations
    # path 
    DATA_PATH = os.path.join(PROJECT_PATH, "data/raw")

    # read uuid
    uuid_file = os.path.join(PROJECT_PATH, "backend/uuid.json")
    uuid_json = helper.read_json(uuid_file)

    # fetch geodata_names 
    geodata_names = list(uuid_json["database"].keys())
    print(geodata_names)

    for geodata_name in geodata_names : 
        geodata_abs_dir = os.path.join(DATA_PATH, geodata_name)

        # uuid df associted to geodata
        uuid_df = pd.DataFrame(uuid_json["database"][geodata_name]["fields"]).transpose().reset_index()
        print(uuid_df)

        # create bounds
        for uuid in uuid_df["uuid"].values : 
            raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_name, uuid)
            print(map_p)

            # set map config json 
            set_mapConfig(temp, map_p, to_js=False, overwrite=False)