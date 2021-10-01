import os
import sys
import jinja2
import pandas as pd
import geopandas as gpd
from IPython.display import display
# path 
PROJ_ABS_PATH = os.path.split((os.path.split(os.getcwd())[0]))[0]
DATA_ABS_PATH = os.path.join(PROJ_ABS_PATH, "database/data")
TEMPLATE_ABS_PATH = os.path.join(PROJ_ABS_PATH, "frontend/templates")
DELIVERABLE_REL_PATH = os.path.join(PROJ_ABS_PATH, "backend/report_deliverable")
sys.path.append(TEMPLATE_ABS_PATH)

# read data
field_data = os.path.join(DATA_ABS_PATH, "raw/Polygo_BOHOUSSOU KOUAME CELESTIN.shp")
data = gpd.read_file(field_data)
print("\n")
print("data loading ...")
display(data)
display(data.columns)

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

# jinja env setting up
search_path = TEMPLATE_ABS_PATH
templateLoader = jinja2.FileSystemLoader(searchpath=search_path)
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "report2.html"
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
    info_etablissement=date_etablissement, info_edition=date_edition)

report_html = os.path.join(DELIVERABLE_REL_PATH, "report_deliv.html")
with open(report_html, "w+") as report:
    report.write(outputText)