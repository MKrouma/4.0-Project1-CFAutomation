#!/bin/bash
# activate virtual env
echo "activate virtual env ..."
cd ..
env/bin/activate

# execute python code
echo "execute backend python code ..."
cd ..
cd backend/
python report_module/render_html.py

# export
echo "export pdf ..."
cd report_deliverable
weasyprint report_deliv.html report.pdf