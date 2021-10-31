import os
import geojson
import requests
from helper import simplifyGeojson

def create_url(provider, data):
    # provider temp URL
    GMAP_URL = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom={}&size={}x{}&maptype=satellite&key={}"
    MAPBOX_URL = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/geojson({})/{},{},{},0/{}x{}?access_token={}"

    # create curl for google map
    if provider == "gmap" :
        url = GMAP_URL
        url_format = url.format(data["lat"], 
                                data["lon"], 
                                data["zoom"], 
                                data["size_w"],
                                data["size_h"],
                                data["key"])  

    # create curl for mapbox
    if provider == "mapbox" :
        url = MAPBOX_URL
        url_format = url.format(data["geojson"],
                                data["lon"], 
                                data["lat"], 
                                data["zoom"], 
                                data["size_w"],
                                data["size_h"],
                                data["key_mapbox"]) 

    if provider not in ["gmap", "mapbox"] :
        print("Enter a proper provider name")
    return url_format

def save_image(provider, data, image_name, overwrite=False, format="png"):

    # get url for provider
    url = create_url(provider, data)
    print(url)

    # request static image
    if overwrite==True and not os.path.exists(image_name) :
        r = requests.get(url)
        # f = open('%s.png' % image_name,'wb')
        f = open('{}.{}'.format(image_name, format),'wb')
        f.write(r.content)
        f.close()
        print(f"{image_name} created !")
    else :
        print(f"{image_name} exists !")



################################### APPLICATION ################################
# simplify-gejson
simplifyGeojson(False)

# dataset
with open("./../database/data/temp/field_data_repaired.geojson") as f:
    gj = geojson.load(f)
# add color
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

print(gj.keys())
print(gj["features"][0])

# data
data = {"geojson": gj,
        "lat": 6.755331569175543, 
        "lon": -4.530004939961217, 
        "zoom": 15.5, 
        "size_w" : 700,
        "size_h": 700,
        "key":"AIzaSyCdnVX6p6LQ9v5NhwL-wJtijkCsmKw4_rU",
        "key_mapbox":"pk.eyJ1IjoibWFoYWRvdSIsImEiOiJja3RwcmVqemIwM3dyMzFrZ2syNzJkZmNpIn0.jbkeDS5DWkOiJxqo8K87cA"
}
provider =  "mapbox" #"mapbox" #"gmap"
image_name = f"./../database/data/map/img_{provider}" 

# function save 
save_image(provider, data, image_name, False)