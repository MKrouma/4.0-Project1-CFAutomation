import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

from module import helper
from backend.python.settings import PROJECT_PATH


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


if __name__ == "__main__" :
    # Data_path and geodata directory
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

        # create bounds
        for uuid in uuid_df["uuid"].values : 
            raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_abs_dir, uuid)

            # # create bounds 
            create_bounds(raw, temp, uuid, to_js=False, overwrite=False)
