import os
import sys
import jinja2
import pandas as pd
import geopandas as gpd

# path 
PROJ_ABS_PATH = os.path.dirname(os.getcwd())
DATA_ABS_PATH = os.path.join(PROJ_ABS_PATH, "database/data")
TEMPLATE_ABS_PATH = os.path.join(PROJ_ABS_PATH, "frontend/templates")
DELIVERABLE_REL_PATH = os.path.join(PROJ_ABS_PATH, "deliverable")
sys.path.append(TEMPLATE_ABS_PATH)

# read data
field_data = os.path.join(DATA_ABS_PATH, "raw/Polygo_BOHOUSSOU KOUAME CELESTIN.shp")
data = gpd.read_file(field_data)
print("\n")
print("data loading ...")
print(data)
print(data.columns)

# read bounds data
bounds_data = os.path.join(DATA_ABS_PATH, "raw/" + os.path.split(field_data)[-1].replace(".shp", "_bounds.shp").replace(" ", "_"))
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
gmap_image = "./../database/data/map/img_mapbox.png"

# jinja env setting up
search_path = TEMPLATE_ABS_PATH
templateLoader = jinja2.FileSystemLoader(searchpath=search_path)
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "report.html"
template = templateEnv.get_template(TEMPLATE_FILE)

# change os dir
# os.chdir(search_path)
# print(f"new chdir {search_path}")

# render template
outputText = template.render(
    num_certif=id, info_programme=programme, info_region=region,
    info_departement=departement, info_sp=sous_prefecture,
    info_village=village, info_dossier=dossier,
    info_demandeur=demandeur, info_CF=CF,
    info_idufci=IDUFCI, info_tf=TF, 
    info_etablissement=date_etablissement, info_edition=date_edition,
    gmap_image=gmap_image,
    bounds_dict=bounds_dict)

report_html = os.path.join(DELIVERABLE_REL_PATH, "report_deliv.html")
with open(report_html, "w+") as report:
    report.write(outputText)