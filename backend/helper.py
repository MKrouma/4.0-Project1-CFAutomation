# map automation modules helper
# import
import os
import uuid
import json
import geojson
import pandas as pd
import geopandas as gpd
from configuration import PROJECT_PATH
from shapely.geometry import Polygon, MultiPolygon, Point, GeometryCollection, LineString

# fill boundaries in dataframe
def fill_boundaries_df(poly_boundaries, log=False) :
    
    # fill dataframe with Bornes informations
    number_of_sommet = len(poly_boundaries)
    Bornes = []
    X = []
    Y = []
    for i in range(number_of_sommet) :
        borne = "B" + str(i+1)
        x = poly_boundaries[i][0]
        y = poly_boundaries[i][1]

        # append
        Bornes.append(borne)
        X.append(x)
        Y.append(y)
    
    # log
    if log :
        print("We have {} sommets in our polygon.".format(number_of_sommet))
    return Bornes, X, Y


# calculer distance
def calculate_dist(gdf) :
    # dist 
    Dist = []
    
    # loop
    for i in list(gdf.index) :
        if i != 0 :

            # take point bi
            bi_moins_1 = gdf.loc[i-1, "geometry"]

            # take point bi
            bi = gdf.loc[i, "geometry"]

            # calcul dist bi-1 - bi
            dist = bi.distance(bi_moins_1)

            # append
            Dist.append(dist)
            
        else :
            Dist.append("N/A")
            
    return Dist

# create file name for boundaries
def create_file_name(gdf, poly_index, desti_folder) :
    village, nom, objectid = gdf.loc[poly_index,"VILLAGE"], gdf.loc[poly_index,"NOM"], gdf.loc[poly_index,"OBJECTID"]
    file_dir = os.path.join(desti_folder, str(objectid) + "_" + village.lower() + "_" + nom.lower())
    
    return file_dir

# create geometry collection
def geometry_collection(list_objects):
    return GeometryCollection(list_objects) 

# create MultiPolygon
def multipolygon(list_objects):
    return MultiPolygon(list_objects) 


# tarnsform data from geojson to js
def transform_geojson_to_js(geojson_path,string):
    with open(geojson_path,'r') as f:

        # variables
        gejson_dirname = os.path.dirname(geojson_path)
        gejson_basename = os.path.basename(geojson_path)
        gejson_extension = gejson_basename.split(".")[-1]

        # transform
        js_path = os.path.join(gejson_dirname, 
        gejson_basename.replace(gejson_extension, "js"))
        
        with open(js_path,'w') as f2: 
            f2.write(string)
            f2.write(f.read())
    return js_path

# simplify geojson
def simplifyGeojson(temp_dir, parameter=[0.001,0.01], overwrite=False) :
    # current and temp directory
    c_dir = os.getcwd()

    if not os.path.exists(os.path.join(temp_dir, "field_data_repaired.geojson")) or overwrite==True : 
        
        # change dir to temp
        os.chdir(temp_dir)

        # simplify field_data
        cmd = f"cat field_data.geojson | simplify-geojson -t {parameter[0]} > field_data_repaired.geojson"
        os.system(cmd)

        # simplify field_bounds
        cmd = F"cat field_bounds.geojson | simplify-geojson -t {parameter[1]} > field_bounds_repaired.geojson"
        os.system(cmd)

        # change dir to current
        os.chdir(c_dir)

        # print
        print("field_data & field_bounds simplified ")

# read geojson file
def read_geojson(file) :
    with open(file) as f:
        gj = geojson.load(f)
    return gj

# read json
def read_json(file) :
    with open(file) as f:
        data = json.load(f)
    return data

# save json
def save_json(file, data) :
    with open(file, 'w') as fp:
        json.dump(data, fp)
    

# makedir func
def mkdir(dir_path, dir_name) :
    # dir abs path
    dir = os.path.join(dir_path, dir_name)

    if not os.path.exists(dir) :
        os.makedirs(dir)
        print(f"{dir} created !")
    else : 
        print(f"{dir} exists !")

    return dir

# utils function
# get field raw and temp path
def get_field_dir(data_path, geodata_dir, idx) :
    field_raw_path = os.path.join(os.path.join(data_path, geodata_dir), f"field_{idx+1}/raw")
    field_temp_path = os.path.join(os.path.join(data_path, geodata_dir), f"field_{idx+1}/temp")
    field_map_path = os.path.join(os.path.join(data_path, geodata_dir), f"field_{idx+1}/map")
    field_deliv_path = os.path.join(os.path.join(data_path, geodata_dir), f"field_{idx+1}/deliv")

    return field_raw_path, field_temp_path, field_map_path, field_deliv_path

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


    if provider not in ["gmap", "mapbox"] :
        print("Enter a proper provider name")
        
    return url_map, url_overview


# generate uuid func
def generate_uuid(uuid_file) :
        
    # read uuid_json
    uuid_json = read_json(uuid_file)

    # generate uuid
    uuid_generated = str(uuid.uuid4())

    # # empty dict
    # uuid_json["database"][uuid_generated] = {}

    # # upgrade uuid_json
    # uuid_json["database"][uuid_generated]["id"] = name
    # uuid_json["database"][uuid_generated]["parent"] = feature_key

    # # write in uuid
    # save_json(uuid_file, uuid_json)

    # # log
    # print(f"{name} created !")
    
    # else :
    #     uuid_generated = uuid_json["database"][name]["id"]
    #     print(f"{name} exists !")

    # # print
    # print(uuid_json)
    return uuid_generated