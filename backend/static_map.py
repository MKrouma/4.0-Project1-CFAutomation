import os
import json
import geojson
import requests
import helper
from configuration import PROJECT_PATH
from backend_utils import static_image

# Data_path and geodata directory
DATA_PATH = os.path.join(PROJECT_PATH, "database/data")
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

        # read map_config
        map_config_file = os.path.join(map_p, "map_config.json")
        map_config = helper.read_json(map_config_file)

        # simplify-gejson
        helper.simplifyGeojson(temp, parameter=[0.001,0.01], overwrite=False)

        # dataset
        data_gj = helper.read_geojson(os.path.join(temp, "field_data.geojson"))
        bounds_gj = helper.read_geojson(os.path.join(temp, "field_bounds.geojson"))
        # data_gj = helper.read_geojson(os.path.join(temp, "field_data_repaired.geojson"))
        # bounds_gj = read_geojson("./../database/data/temp/field_bounds_repaired.geojson")

        # stylying overlay
        # gj["properties"] = {}
        # gj["properties"]["fill"] = "#555555"
        # gj["properties"]["fill-opacity"] = 0.6
        # gj["features"][0]["properties"] = {}
        # gj["features"][0]["properties"]["stroke"] = "FFFAFA"
        # gj["features"][0]["properties"]["stroke-opacity"] = 1.0
        # gj["features"][0]["properties"]["stroke-width"] = 5.0
        # gj["features"][0]["properties"]["fill"] = "#7e7e7e"
        # gj["features"][0]["properties"]["fill-opacity"] = 0.9
        # gj["features"][0]["style"] = {}
        # gj["features"][0]["style"]["fill"] = "red"
        # gj["features"][0]["style"]["fill-opacity"] = 0.9

        # data_map
        data_map = {"data_geojson": data_gj,
                    "bounds_geojson": bounds_gj,
                    "lat": map_config["center"]["lat"], 
                    "lon": map_config["center"]["lon"], 
                    "zoom": 15.5, 
                    "size_w" : 700,
                    "size_h": 700,
                    "key":"AIzaSyCdnVX6p6LQ9v5NhwL-wJtijkCsmKw4_rU",
                    "key_mapbox":"pk.eyJ1IjoibWFoYWRvdSIsImEiOiJja3RwcmVqemIwM3dyMzFrZ2syNzJkZmNpIn0.jbkeDS5DWkOiJxqo8K87cA"
        }

        # data_overview
        data_overview = {"data_geojson": data_gj,
                        "bounds_geojson": bounds_gj,
                        "lat": map_config["center"]["lat"], 
                        "lon": map_config["center"]["lon"], 
                        "zoom": 12, 
                        "size_w" : 300,
                        "size_h": 200,
                        "key":"AIzaSyCdnVX6p6LQ9v5NhwL-wJtijkCsmKw4_rU",
                        "key_mapbox":"pk.eyJ1IjoibWFoYWRvdSIsImEiOiJja3RwcmVqemIwM3dyMzFrZ2syNzJkZmNpIn0.jbkeDS5DWkOiJxqo8K87cA"
        }

        # get url for provider
        provider =  "mapbox" #"mapbox" #"gmap"

        # get map & overview url
        url_map, url_overview = helper.create_url(provider, data_map, data_overview) 

        # # function save 
        map_img = os.path.join(map_p, f"map_{provider}") 
        overview_img = os.path.join(map_p, f"overview_{provider}")

        # static image for map & overview
        static_image(url_map, map_img, False)
        static_image(url_overview, overview_img, False)