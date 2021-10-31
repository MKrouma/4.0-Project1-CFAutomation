import os
import geojson
import requests
from helper import simplifyGeojson, read_geojson

# simplify-gejson
simplifyGeojson(parameter=0.001, type="data", overwrite=False)
simplifyGeojson(parameter=0.01, type="bounds", overwrite=False)

# dataset
data_gj = read_geojson("./../database/data/temp/field_data_repaired.geojson")
bounds_gj = read_geojson("./../database/data/temp/field_bounds.geojson")
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
            "lat": 6.755331569175543, 
            "lon": -4.530004939961217, 
            "zoom": 15.5, 
            "size_w" : 700,
            "size_h": 700,
            "key":"AIzaSyCdnVX6p6LQ9v5NhwL-wJtijkCsmKw4_rU",
            "key_mapbox":"pk.eyJ1IjoibWFoYWRvdSIsImEiOiJja3RwcmVqemIwM3dyMzFrZ2syNzJkZmNpIn0.jbkeDS5DWkOiJxqo8K87cA"
}

# data_overview
data_overview = {"data_geojson": data_gj,
                "bounds_geojson": bounds_gj,
                "lat": 6.755331569175543, 
                "lon": -4.530004939961217, 
                "zoom": 12, 
                "size_w" : 300,
                "size_h": 200,
                "key":"AIzaSyCdnVX6p6LQ9v5NhwL-wJtijkCsmKw4_rU",
                "key_mapbox":"pk.eyJ1IjoibWFoYWRvdSIsImEiOiJja3RwcmVqemIwM3dyMzFrZ2syNzJkZmNpIn0.jbkeDS5DWkOiJxqo8K87cA"
}

# get url for provider
provider =  "mapbox" #"mapbox" #"gmap"

def create_url(provider, data_map, data_overview):
    # provider temp URL
    GMAP_URL = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom={}&size={}x{}&maptype=satellite&key={}"
    MAPBOX_URL = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/geojson({})/{},{},{},0/{}x{}?access_token={}"
    MAPBOX_URL2 = "https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/static/geojson({})/{},{},{},0/{}x{}?access_token={}"

    # url map & overview
    url_map = None
    url_overview = None

    # create curl for google map
    if provider == "gmap" :
        url_map = GMAP_URL.format(data_map["lat"], 
                                data_map["lon"], 
                                data_map["zoom"], 
                                data_map["size_w"],
                                data_map["size_h"],
                                data_map["key"])  
        
        # overview
        url_overview = GMAP_URL.format(data_overview["lat"], 
                                    data_overview["lon"], 
                                    data_overview["zoom"], 
                                    data_overview["size_w"],
                                    data_overview["size_h"],
                                    data_overview["key"]) 

    # create curl for mapbox
    if provider == "mapbox" :
        # map 
        url_map = MAPBOX_URL.format(data_map["data_geojson"],
                                data_map["lon"], 
                                data_map["lat"], 
                                data_map["zoom"], 
                                data_map["size_w"],
                                data_map["size_h"],
                                data_map["key_mapbox"]) 
        
        # overview
        url_overview = MAPBOX_URL2.format(data_overview["data_geojson"],
                                        data_overview["lon"], 
                                        data_overview["lat"], 
                                        data_overview["zoom"], 
                                        data_overview["size_w"],
                                        data_overview["size_h"],
                                        data_overview["key_mapbox"]) 

        # map overview


    if provider not in ["gmap", "mapbox"] :
        print("Enter a proper provider name")
    return url_map, url_overview

url_map, url_overview = create_url(provider, data_map, data_overview) 

# create static_image
def static_image(url, img_name, overwrite=False, format="png"):
    # request static image
    if overwrite==True and not os.path.exists(img_name) :
        r = requests.get(url)
        # f = open('%s.png' % image_name,'wb')
        f = open('{}.{}'.format(img_name, format),'wb')
        f.write(r.content)
        f.close()
        print(f"{img_name} created !")
    else :
        print(f"{img_name} exists !")

# # function save 
map_img = f"./../database/data/map/map_{provider}" 
overview_img = f"./../database/data/map/overview_{provider}"

# static image for map & overview
static_image(url_map, map_img, True)
static_image(url_overview, overview_img, True)