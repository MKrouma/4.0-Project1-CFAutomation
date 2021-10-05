# 4.0-Team

## Description


## Table of content
* Automation 
* Backend 
* Databse 
* Frontend 


## How to run
Get this project from Github and clone it.\
`git clone https://github.com/MKrouma/4.0-Project1-CFAutomation.git`

### Staging directory
cd automation/staging

### Create a venv env
python -V\
python -m venv env

Be sure to call your virtual environment as "env". Because we're using this in the 
bash script. We can't change it later. Otherwise, change your env with env name in the
bash script.

### Activate your virtual
source env/bin/activate\
-- windows : env/bin/activate

### Install requirements
which pip (that's to verify that pip is running in your virtual env)\
-- windows : where pip\
pip install -r automation/requirements_dev.txt

### Create new git branch and push 
git checkout -b YOUR_NAME_DEV_BRANCH (YOUR_NAME to change)\
git add .\
git commit -m "message"\
git push -u origin YOUR_NAME_DEV_BRANCH


## Run
To use you just have to in 'automation/staging' folder and run create_pdf_report.sh bash script. 

Until the code is in production, we have some things to change right now. 

### frontend/templates/report2.html
--> go to frontend/templates/report2.html\
--> change the dirname path with your absolute path.\
i.e : "/Users/mac/Documents/PROJET/4.0-Project1-CFAutomation/frontend/statics/css/report2.css">\
change : "{YOUR_ABS_PATH}/frontend/statics/css/report2.css">\
--> Do that also for armoirie-logo and afor-logo in html body.

### run bash_script (in automation/staging directory)
bash create_pdf_report.sh\
-- windows : create_pdf_report.bat

### Result
--> frontend/templates/report2.html : run it in your browser to see how it's looking.
--> backend/report_deliverable/report_deliv.html : show how the html file is looking with jinja rendering.
--> backend/report_deliverable/report_deliv.html : show how the final pdf report should look. A lot of things to change.


## Author
4.0 Team 
