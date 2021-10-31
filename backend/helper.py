# map automation modules helper
# import
import os
import geojson
import pandas as pd
import geopandas as gpd
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
def simplifyGeojson(parameter=0.001, type="data", overwrite=False) :
    # current and temp directory
    c_dir = os.getcwd()
    temp_dir = os.path.join(os.path.dirname(os.getcwd()), "database/data/temp/")

    if type == "data" :
        if not os.path.exists("./../database/data/temp/field_data_repaired.geojson") or overwrite==True: 
            
            # change dir to temp
            os.chdir(temp_dir)

            # command line
            cmd = f"cat field_data.geojson | simplify-geojson -t {parameter} > field_data_repaired.geojson"
            os.system(cmd)

            # change dir to current
            os.chdir(c_dir)

            # print
            print("field_data.geojson simply to field_data_repaired.geojson")

    if type == "bounds" :
        if not os.path.exists("./../database/data/temp/field_bounds_repaired.geojson") or overwrite==True: 
            
            # change dir to temp
            os.chdir(temp_dir)

            # command line
            cmd = "cat field_bounds.geojson | simplify-geojson -t 0.001 > field_bounds_repaired.geojson"
            os.system(cmd)

            # change dir to current
            os.chdir(c_dir)

            # print
            print("field_bounds.geojson simply to field_bounds_repaired.geojson")


# read geojson file
def read_geojson(file) :
    with open(file) as f:
        gj = geojson.load(f)
    return gj

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

