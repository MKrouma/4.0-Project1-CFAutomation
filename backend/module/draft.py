import os
import geopandas as gpd
from backend.python.settings import PROJECT_PATH

gdf = gpd.read_file(os.path.join(PROJECT_PATH, 
"database/data/totokro/0f370b6a-636f-491b-a8e3-afca29c0a931/raw/totokro.shp"))

print(gdf["uuid"])
