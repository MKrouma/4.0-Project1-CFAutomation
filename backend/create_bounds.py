import os
import sys
import helper
import numpy as np
import pandas as pd
import geopandas as gpd
from backend_utils import create_bounds
from configuration import PROJECT_PATH


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
    print("\n")
    print(f"number of fields : {number_fields}")
    print(f"existing sub-directories : {list_dir}")

    # get field raw & temp
    for idx in range(number_fields) : 
        raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_dir, idx)

        # create bounds 
        create_bounds(raw, temp, idx, to_js=False, overwrite=True)