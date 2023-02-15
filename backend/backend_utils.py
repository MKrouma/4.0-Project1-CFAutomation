import os
import sys
import json
import helper
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from backend.python.settings import PROJECT_PATH

## 1. create directories utils
def dirGeoData(data_shp, extern_path, data_path, uuid_file) :
    # UUID_json 
    uuid_json = helper.read_json(uuid_file)

    # organize directory for each geodata
    geodata_file = os.path.join(extern_path, data_shp)

    # MAKE PARENT DIRECTORY
    # geodata name
    geodata_name = data_shp.replace(".shp", "").lower()

    # create geodata dir & generate uuid
    if geodata_name not in uuid_json["database"].keys() :
        uuid_gen = helper.generate_uuid(uuid_file)

        # create geodata directory
        geodata_dir = helper.mkdir(data_path, geodata_name)

        # fill uuid_json
        uuid_json["database"][geodata_name] = {}
        uuid_json["database"][geodata_name]["uuid"] = uuid_gen
        uuid_json["database"][geodata_name]["fields"] = {}

        # MAKE SUB DIRECTORIES
        # create fields directories
        geodata_gpd = gpd.read_file(geodata_file)
        number_fields = geodata_gpd.shape[0]

        for idx in range(number_fields) :
            # existing fields
            geodata_fields_created = uuid_json["database"][geodata_name]["fields"].keys()

            # field name
            field_name = f"field_{idx+1}"

            # generate field uuid and make directory
            if field_name not in geodata_fields_created :
                uuid_gen = helper.generate_uuid(uuid_file)

                # create field 
                field_uuid_dir = helper.mkdir(geodata_dir, uuid_gen)

                # create map, raw, temp subdirectories
                _ = helper.mkdir(field_uuid_dir, "map")
                _ = helper.mkdir(field_uuid_dir, "temp")
                _ = helper.mkdir(field_uuid_dir, "deliv")
                _ = helper.mkdir(field_uuid_dir, "raw")

                # copy raw data
                geodata_gpd.to_file(os.path.join(_, geodata_name + ".shp"))

                # fill json
                uuid_json["database"][geodata_name]["fields"][field_name] = {}
                uuid_json["database"][geodata_name]["fields"][field_name]["uuid"] = uuid_gen
                uuid_json["database"][geodata_name]["fields"][field_name]["parent"] = geodata_name

                print(f"{field_uuid_dir} created !")

        # write uuid_json
        helper.save_json(uuid_file, uuid_json)

    else : 
        print(f"{geodata_name} existed !")

    # create new raw data with uuid
    uuid_df = pd.DataFrame(uuid_json["database"][geodata_name]["fields"]).transpose().reset_index()

    # affected uuid 
    geodata_gpd = gpd.read_file(geodata_file)
    geodata_gpd["uuid"] = uuid_df["uuid"].values

    # copy raw data
    for uuid in uuid_df["uuid"].values : 

        # uuid raw dir
        uuid_raw_dir = os.path.join(os.path.join(PROJECT_PATH, "database/data"), geodata_name)
        uuid_raw_dir = os.path.join(os.path.join(uuid_raw_dir, uuid), "raw")
        geodata_gpd.to_file(os.path.join(uuid_raw_dir, geodata_name + ".shp"))
        


## 2. create boundaries utils
# create_bounds_func
def create_bounds(field_raw_path, field_temp_path, uuid, to_js=False, overwrite=False) :
    # geodata file
    geodata_file = [file for file in os.listdir(field_raw_path) if file[-4:]==".shp"]
    geodata_file = geodata_file[0].replace("_bounds","")

    # read gdf
    field_data = os.path.join(field_raw_path, geodata_file)
    data = gpd.read_file(field_data)

    # get poly bounds
    data_uuid = data[data["uuid"] == uuid]
    poly_index = data_uuid.index[0]

    poly_shapely = data_uuid.loc[poly_index,"geometry"]
    poly_boundaries = list(np.asarray(poly_shapely.exterior.coords)[:-1])
    poly_boundaries = [list(line) for line in poly_boundaries]

    # empty dataframe to fill
    df = pd.DataFrame(columns=["OBJECTID", "Bornes", "X", "Y", "Distance"])

    # get Bornes, X & Y informations
    Bornes, X, Y = helper.fill_boundaries_df(poly_boundaries)

    # fill df
    df["Bornes"] = Bornes
    df["X"] = X
    df["Y"] = Y

    # objectID
    df["OBJECTID"] = data_uuid["OBJECTID"]

    # transform to geodataframe
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X, df.Y))

    # ingest distance
    gdf["Distance"] = helper.calculate_dist(gdf)

    # rename gdf
    new_columns = ["Bornes", "X(m)", "Y(m)", "Distance(m)"]
    gdf = gdf.rename(columns={"X":"X(m)", "Y":"Y(m)", "Distance":"Distance(m)"})

    # save brut bounds with local EPSG
    bounds_raw_file = os.path.join(field_raw_path, os.path.split(field_data)[-1].replace(".shp", "_bounds.shp").replace(" ", "_"))
    if not os.path.exists(bounds_raw_file) or overwrite==True:
        gdf.to_file(bounds_raw_file)
        print(f"{bounds_raw_file} created !")

    # change crs
    gdf.set_crs("epsg:32630", inplace=True)
    gdf.to_crs("epsg:4326", inplace=True)
    gdf["lat"] = gdf["geometry"].apply(lambda point : point.y)
    gdf["lon"] = gdf["geometry"].apply(lambda point : point.x)

    gdf = gdf[["OBJECTID", "Bornes", "lat", "lon", "geometry"]]


    # save bounds data as geojson
    bounds_file = "field_bounds.geojson"
    bounds_file = os.path.join(field_temp_path, bounds_file)
    bounds_geojson = gdf.copy()

    if not os.path.exists(bounds_file) or overwrite==True :
        bounds_geojson.to_file(bounds_file, driver='GeoJSON')
        print(f"{bounds_file} created !")

    # save original data as geojson
    data_geojson = data.loc[[poly_index]].to_crs("epsg:4326")
    data_file = "field_data.geojson"
    data_file = os.path.join(field_temp_path, data_file)

    if not os.path.exists(data_file) or overwrite==True :
        data_geojson.to_file(data_file, driver='GeoJSON')
        print(f"{data_file} created !")
    else : 
        print(f"{data_file} exists !")

    # transform geojson to js for Leaflet layers
    if to_js :
        js_path = helper.transform_geojson_to_js(data_file,"var field_data = ")
        js_path = helper.transform_geojson_to_js(bounds_file,"var field_bounds = ")



## 3. set map configurations utils
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


## 4. render static map utils
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


## 5. render html utils



## 6. transform html to pdf utils