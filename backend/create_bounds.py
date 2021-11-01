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
