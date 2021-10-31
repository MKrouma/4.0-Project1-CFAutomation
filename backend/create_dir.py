import os
import geopandas as gpd
from helper import mkdir
from backend_utils import dirGeoData
from configuration import PROJECT_PATH

# directory
EXTERN_PATH = os.path.join(PROJECT_PATH, "database/extern")
DATA_PATH = os.path.join(PROJECT_PATH, "database/data")

# geodata file in extern directory
LIST_GEODATA = [file for file in os.listdir(EXTERN_PATH) if file[-4:]==".shp"]

# create fild for each geodata
for data_name in LIST_GEODATA : 
    print(f"{data_name} setting up necessary directories ...")
    dirGeoData(data_name, EXTERN_PATH, DATA_PATH)