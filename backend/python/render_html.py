import os
import sys
import jinja2
import pandas as pd
import geopandas as gpd

from module import helper
from configuration import PROJECT_PATH

# local_dir
local_dir = os.getcwd()

# Data_path and geodata directory
DATA_PATH = os.path.join(PROJECT_PATH, "database/data")
# read uuid
uuid_file = os.path.join(PROJECT_PATH, "backend/uuid.json")
uuid_json = helper.read_json(uuid_file)

# fetch geodata_names 
geodata_names = list(uuid_json["database"].keys())
print(geodata_names)

# path 
TEMPLATE_ABS_PATH = os.path.join(PROJECT_PATH, "frontend/templates")
DELIVERABLE_REL_PATH = os.path.join(PROJECT_PATH, "deliverable")
sys.path.append(TEMPLATE_ABS_PATH)


for geodata_name in geodata_names : 
    geodata_abs_dir = os.path.join(DATA_PATH, geodata_name)

    # uuid df associted to geodata
    uuid_df = pd.DataFrame(uuid_json["database"][geodata_name]["fields"]).transpose().reset_index()
    print(uuid_df)

    # create bounds
    for uuid in uuid_df["uuid"].values : 
        raw, temp, map_p, deliv = helper.get_field_dir(DATA_PATH, geodata_name, uuid)
        geodata_file = [file for file in os.listdir(raw) if file[-4:]==".shp"]
        geodata_file = geodata_file[0].replace("_bounds","")

        # read data
        field_data = os.path.join(raw, geodata_file)
        data = gpd.read_file(field_data)
        print("\n")
        print("data loading ...")
        print(data)
        print(data.columns)

        # read bounds data
        bounds_data = os.path.join(raw, geodata_file.replace(".shp", "_bounds.shp"))
        bounds = gpd.read_file(bounds_data)

        # round X, Y & Distance
        bounds["X(m)"] = bounds["X(m)"].apply(lambda x : round(x,2))
        bounds["Y(m)"] = bounds["Y(m)"].apply(lambda x : round(x,2))
        bounds["Distance(m"] = bounds["Distance(m"].apply(lambda x : round(float(x),3) if x!="N/A" else "")

        # transfrom to dict
        keep_cols = ["Bornes", "X(m)", "Y(m)", "Distance(m"]
        bounds_dict = bounds[keep_cols].to_dict(orient="index")

        # template variables
        id = data.loc[0, "id"]
        programme       = "PAMOFOR"
        region          = data.loc[0, "REGION"]    
        departement     = data.loc[0, "DEPARTEMEN"]     
        sous_prefecture = data.loc[0, "SOUS_PREF"]     
        village         = data.loc[0, "VILLAGE"]    
        dossier         = None    
        demandeur       = data.loc[0, "NOM"]  
        CF              = None
        IDUFCI          = None
        TF              = None
        date_etablissement = "30/09/2021"
        date_edition       = "30/09/2021"
        map_mapbox = os.path.join(map_p, "map_mapbox.png")
        overview_mapbox = os.path.join(map_p, "overview_mapbox.png") 

        # jinja env setting up
        search_path = TEMPLATE_ABS_PATH
        templateLoader = jinja2.FileSystemLoader(searchpath=search_path)
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "report.html"
        template = templateEnv.get_template(TEMPLATE_FILE)

        # change os dir
        os.chdir(search_path)
        print(f"new chdir {search_path}")

        # render template
        outputText = template.render(
            num_certif=id, info_programme=programme, info_region=region,
            info_departement=departement, info_sp=sous_prefecture,
            info_village=village, info_dossier=dossier,
            info_demandeur=demandeur, info_CF=CF,
            info_idufci=IDUFCI, info_tf=TF, 
            info_etablissement=date_etablissement, info_edition=date_edition,
            overview_mapbox=overview_mapbox,
            map_mapbox=map_mapbox,
            bounds_dict=bounds_dict)

        report_html = os.path.join(deliv, "report_deliv.html")
        with open(report_html, "w+") as report:
            report.write(outputText)

        # change os dir
        os.chdir(search_path)
        print(f"new chdir {search_path}")