#!/bin/bash
# activate virtual env
echo "activate virtual env ..."
source env/bin/activate

# execute python code
echo "execute backend python code ..."
cd backend
python render_html.py

# export
echo "export pdf ..."
cd ../deliverable
weasyprint report_deliv.html report.pdf