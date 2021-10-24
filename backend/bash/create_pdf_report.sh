#!/bin/bash

cd ..
echo "1. Run map configurations."
python map_config.py
echo "map configurations !"
echo

# go to project path
cd ..

# execute python code
echo "2. Execute render_html code."
cd backend
python render_html.py
echo "html rendering done with jinja !"
echo

# export
echo "3. Export pdf."
cd ../deliverable
/usr/local/bin/weasyprint report_deliv.html report.pdf
echo
echo "report.pdf in deliverable with some warning, for sure :) !"