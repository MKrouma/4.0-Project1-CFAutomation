import os
import geopandas as gpd
from helper import mkdir
from configuration import PROJECT_PATH

# directory
EXTERN_PATH = os.path.join(PROJECT_PATH, "database/extern")
DATA_PATH = os.path.join(PROJECT_PATH, "database/data")

# geodata file in extern directory
LIST_GEODATA = [file for file in os.listdir(EXTERN_PATH) if file[-4:]==".shp"]

def dirGeoData(data_name, extern_path, data_path) :
    # organize directory for each geodata
    GEODATA_FILE = os.path.join(extern_path, data_name)
    print(GEODATA_FILE)

    # create geodata directory
    geodata_name = os.path.split(GEODATA_FILE)[-1].replace(" ", "_").replace(".shp", "").lower()
    print(geodata_name)

    # create geodata directory
    geodata_dir = mkdir(data_path, geodata_name)

    # create fields directories
    geodata_gpd = gpd.read_file(GEODATA_FILE)
    number_fields = geodata_gpd.shape[0]

    for idx in range(number_fields) :
        # create field 
        field_idx_dir = mkdir(geodata_dir, f"field_{idx+1}")

        # create map, raw, temp subdirectories
        _ = mkdir(field_idx_dir, "map")
        _ = mkdir(field_idx_dir, "temp")
        _ = mkdir(field_idx_dir, "deliv")
        _ = mkdir(field_idx_dir, "raw")

        # copy raw data
        geodata_gpd.to_file(os.path.join(_, geodata_name + ".shp"))


# create fild for each geodata
for data_name in LIST_GEODATA : 
    print(f"{data_name} setting up necessary directories ...")
    dirGeoData(data_name, EXTERN_PATH, DATA_PATH)