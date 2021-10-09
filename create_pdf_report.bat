#!/bin/bash
# activate virtual env
echo "1. Activate virtual env."
env\Scripts\activate
echo "virtual env created !"
echo

# execute python code
echo "2. Execute html render code."
cd backend
python render_html.py
echo "html rendering done with jinja !"
echo

# run map config
echo "3. Run map configurations."
python map_config.py
echo "map configurations !"
echo

# export
echo "4. Export pdf."
cd ..\deliverable
weasyprint report_deliv.html report.pdf
echo
echo "report.pdf in deliverable with some warning, for sure :) !"