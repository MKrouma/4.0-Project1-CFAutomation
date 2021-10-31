import os
import sys
import helper
import numpy as np
import pandas as pd
import geopandas as gpd
from configuration import PROJECT_PATH

# utils function
# get field raw and temp path
def get_field_dir(data_path, geodata_dir, idx) :
    field_raw_path = os.path.join(os.path.join(data_path, geodata_dir), f"field_{idx+1}/raw")
    field_temp_path = os.path.join(os.path.join(data_path, geodata_dir), f"field_{idx+1}/temp")

    return field_raw_path, field_temp_path

# create_bounds_func
def create_bounds(field_raw_path, field_temp_path, to_js=False) :
    # geodata file
    geodata_file = [file for file in os.listdir(field_raw_path) if file[-4:]==".shp"]
    geodata_file = geodata_file[0].replace("_bounds","")

    # read gdf
    field_data = os.path.join(field_raw_path, geodata_file)
    data = gpd.read_file(field_data)

    # get poly bounds
    poly_index = 0
    poly_shapely = data["geometry"].values[poly_index]
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
    df["OBJECTID"] = data.loc[poly_index, "OBJECTID"]

    # transform to geodataframe
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X, df.Y))

    # ingest distance
    gdf["Distance"] = helper.calculate_dist(gdf)

    # rename gdf
    new_columns = ["Bornes", "X(m)", "Y(m)", "Distance(m)"]
    gdf = gdf.rename(columns={"X":"X(m)", "Y":"Y(m)", "Distance":"Distance(m)"})

    # save brut bounds with local EPSG
    bounds_raw_file = os.path.join(field_raw_path, os.path.split(field_data)[-1].replace(".shp", "_bounds.shp").replace(" ", "_"))
    gdf.to_file(bounds_raw_file)

    # change crs
    gdf.set_crs("epsg:32630", inplace=True)
    gdf.to_crs("epsg:4326", inplace=True)
    gdf["lat"] = gdf["geometry"].apply(lambda point : point.y)
    gdf["lon"] = gdf["geometry"].apply(lambda point : point.x)

    gdf = gdf[["OBJECTID", "Bornes", "lat", "lon", "geometry"]]


    # save as geojson
    bounds_file = "field_bounds.geojson"
    bounds_file = os.path.join(field_temp_path, bounds_file)
    bounds_geojson = gdf.copy()
    bounds_geojson.to_file(bounds_file, driver='GeoJSON')

    # save original data as js too
    data_geojson = data.to_crs("epsg:4326")
    data_file = "field_data.geojson"
    data_file = os.path.join(field_temp_path, data_file)
    data_geojson.to_file(data_file, driver='GeoJSON')

    # transform geojson to js for Leaflet layers
    if to_js :
        js_path = helper.transform_geojson_to_js(data_file,"var field_data = ")
        js_path = helper.transform_geojson_to_js(bounds_file,"var field_bounds = ")

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
    print(number_fields)
    print(list_dir)

    # get field raw & temp
    for idx in range(number_fields) : 
        field_raw_path, field_temp_path = get_field_dir(DATA_PATH, geodata_dir, idx)
        print(f"{field_raw_path} ...\n")

        # create bounds 
        create_bounds(field_raw_path, field_temp_path, to_js=False)