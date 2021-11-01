#!/bin/bash

# backend directory
cd ..

# create directories
python create_dir.py

# create bounds
python create_bounds.py

# set map config
python map_config.py

# get static images
python static_map.py

# render html 
python render_html.py

# transform html to pdf
# weasyprint report_deliv.html report.pdf