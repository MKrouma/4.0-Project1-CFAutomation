#!/bin/bash
# activate virtual env
echo "activate virtual env ..."
source ../env/bin/activate

# execute python code
echo "execute backend python code ..."
cd ../..
cd backend/report_module
python render_html.py
cd ../

# export
echo "export pdf ..."
cd report_deliverable
weasyprint report_deliv.html report.pdf