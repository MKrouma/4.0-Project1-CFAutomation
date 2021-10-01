import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
from IPython.display import display

import helper
DATA_REL_PATH = "./../../database/data"
sys.path.append("DATA_REL_PATH")

# read data
field_data = os.path.join(DATA_REL_PATH, "raw/Polygo_BOHOUSSOU KOUAME CELESTIN.shp")
data = gpd.read_file(field_data)

# get poly bounds
poly_index = 0
poly_shapely = data["geometry"].values[poly_index]
poly_boundaries = list(np.asarray(poly_shapely.exterior.coords)[:-1])
poly_boundaries = [list(line) for line in poly_boundaries]

# empty dataframe to fill
df = pd.DataFrame(columns=["OBJECTID", "Bornes", "X", "Y", "Distance"])

# get Bornes, X & Y informations
Bornes, X, Y = helper.fill_boundaries_df(poly_boundaries)

# fill df
df["Bornes"] = Bornes
df["X"] = X
df["Y"] = Y

# objectID
df["OBJECTID"] = data.loc[poly_index, "OBJECTID"]

# transform to geodataframe
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X, df.Y))

# ingest distance
gdf["Distance"] = helper.calculate_dist(gdf)

# rename gdf
new_columns = ["Bornes", "X(m)", "Y(m)", "Distance(m)"]
gdf = gdf.rename(columns={"X":"X(m)", "Y":"Y(m)", "Distance":"Distance(m)"})

# change crs
gdf.set_crs("epsg:32630", inplace=True)
gdf.to_crs("epsg:4326", inplace=True)
gdf["lat"] = gdf["geometry"].apply(lambda point : point.y)
gdf["lon"] = gdf["geometry"].apply(lambda point : point.x)

gdf = gdf[["OBJECTID", "Bornes", "lat", "lon", "geometry"]]
display(gdf)


# save as geojson
bounds_file = "field_bounds.geojson"
bounds_file = os.path.join(DATA_REL_PATH, "temp/"+bounds_file)
bounds_geojson = gdf.copy()
bounds_geojson.to_file(bounds_file, driver='GeoJSON')

# save original data as js too
data_geojson = data.to_crs("epsg:4326")
data_file = "field_data.geojson"
data_file = os.path.join(DATA_REL_PATH, "temp/"+data_file)
data_geojson.to_file(data_file, driver='GeoJSON')