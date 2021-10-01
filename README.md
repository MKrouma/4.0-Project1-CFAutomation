# 4.0-Team

## Description



## Table of content
### Automation 
One code running. 
Contains staging code : bash script
Virtual environnement
Test folder to test 

### Backend 
Python code.

### Databse 
Data folder.
To transform in a all database later.

### Frontend 
Html templates
Statics : css, js, img

## How to install
To use this project, you have to set up a virtual environnement. 

### Create a venv env
python -V\
python -m venv env\

Be sure to call your virtual environment as "env". Because we're using this in the 
bash script. We can't change it later. Otherwise, change your env with env name in the
bash script.

### Activate your virtual
source env/bin/activate\

### Install requirements
which pip (that's to verify that pip is running in your virtual env)\
pip install -r automation/requirements_dev.txt

### Create new git branch and push 
git checkout -b YOUR_NAME_DEV_BRANCH (YOUR_NAME to change)\
git add .\
git commit -m "message"\
git push -u origin YOUR_NAME_DEV_BRANCH

## How to use 
To use you just have to in 'automation/staging' folder and run create_pdf_report.sh bash script. 

Until the code is in production, we have some things to change right now. 

### frontend/templates/report2.html
--> go to \
--> change the dirname path with your absolute path.\
i.e : "/Users/mac/Documents/PROJET/4.0-Project1-CFAutomation/frontend/statics/css/report2.css">\
change : "{YOUR_ABS_PATH}/frontend/statics/css/report2.css">\
--> Do that also for armoirie-logo and afor-logo in html body.

###

## License
Ya pas license ici ! 
