import os
import json
import geojson
import requests
import pandas as pd

from module import helper
from configuration import PROJECT_PATH


## 4. render static map utils
# create static_image
def static_image(url, img_name, overwrite=False, format="png"):
    # request static image
    if not os.path.exists(img_name) or overwrite==True :
        r = requests.get(url)
        # f = open('%s.png' % image_name,'wb')
        f = open('{}.{}'.format(img_name, format),'wb')
        f.write(r.content)
        f.close()
        print(f"{img_name} created !")
    else :
        print(f"{img_name} exists !")


if __name__ == "__main__" :
    # Data_path and geodata directory
    DATA_PATH = os.path.join(PROJECT_PATH, "database/data")
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

        # fetch uuid (field) for geodata
        for uuid in uuid_df["uuid"].values : 
            raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_name, uuid)

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