#!/bin/bash

# createa map config parameters
cd ..
python map_config.py

# go to project path
cd ..

# execute python code
cd backend
python render_html.py
python static_map.py

# export
cd ../deliverable
# /usr/local/bin/weasyprint report_deliv.html report.pdf
weasyprint report_deliv.html report.pdf