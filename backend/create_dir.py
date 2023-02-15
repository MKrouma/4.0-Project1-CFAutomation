# import helper
import os
import sys
import pandas as pd
import geopandas as gpd
from settings import PROJECT_PATH
from module import helper


## 1. create directories utils
def dirGeoData(file_shp, deliv_path):
    # read 
    print(file_shp)
        
if __name__ == "__main__" :

    # directory
    data_temp_path = os.path.join(PROJECT_PATH, "data/extern")
    data_raw_path = os.path.join(PROJECT_PATH, "data/raw")

    # geodata file in extern directory
    LIST_GEODATA = [file for file in os.listdir(data_raw_path) if file[-4:]==".shp"]
    LIST_GEODATA = LIST_GEODATA[1:]

    # create fild for each geodata
    file_shp = LIST_GEODATA[0]
    dirGeoData(file_shp, data_temp_path)