# import helper
import os
import sys
import pandas as pd
import geopandas as gpd
from configuration import PROJECT_PATH
from module import helper


## 1. create directories utils
def dirGeoData(data_shp, extern_path, data_path, uuid_file) :
    # UUID_json 
    uuid_json = helper.read_json(uuid_file)

    # organize directory for each geodata
    geodata_file = os.path.join(extern_path, data_shp)

    # MAKE PARENT DIRECTORY
    # geodata name
    geodata_name = data_shp.replace(" ", "_").replace(".shp", "").lower()

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
        
if __name__ == "__main__" :

    # directory
    EXTERN_PATH = os.path.join(PROJECT_PATH, "database/extern")
    DATA_PATH = os.path.join(PROJECT_PATH, "database/data")

    # UUID FILE
    UUID_FILE = os.path.join(PROJECT_PATH, "backend/uuid.json")

    # geodata file in extern directory
    LIST_GEODATA = [file for file in os.listdir(EXTERN_PATH) if file[-4:]==".shp"]
    print(LIST_GEODATA)

    # create fild for each geodata
    for data_name in LIST_GEODATA : 
        dirGeoData(data_name, EXTERN_PATH, DATA_PATH, UUID_FILE)