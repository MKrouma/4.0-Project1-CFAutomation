import os
import sys
import json
import helper
import pandas as pd
import geopandas as gpd
from configuration import PROJECT_PATH
from backend_utils import set_mapConfig

# map configurations
# path 
DATA_PATH = os.path.join(PROJECT_PATH, "database/data")

# geodata directories
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
    print("\n")
    print(f"number of fields : {number_fields}")
    print(f"existing sub-directories : {list_dir}")

    # get field raw & temp
    for idx in range(number_fields) : 
        raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_dir, idx)
        print("\n...")
        print(raw)

        # set map config json 
        set_mapConfig(temp, map_p, to_js=False, overwrite=False)