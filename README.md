# 4.0-Team
Project to automation map production for PAMOFOR.


## Table of content
* Backend 
* Database
* Deliverable
* Frontend 


## How to run
Get this project from Github and clone it.\
`git clone https://github.com/MKrouma/4.0-Project1-CFAutomation.git`
Then, go to project folder.

### Create a virtual environment
This can be done with `python -m venv env`
Activate virtual environment with 

```
source env/bin/activate
```
or (for Windows users)
```
env\Scripts\activate
```

### Install requirements
```
pip install -r requirements_dev.txt
```

### Create new git branch for own developement. 
```
git checkout -b {YOUR_NAME}_dev_branch (YOUR_NAME to change)
```

### Manual stuff to change
* go the html file `frontend/templates/report2.html`
* change css, armoirie-logo and afor-logo path
```
<link rel="stylesheet" href="{YOUR_ABS_PATH}/frontend/statics/css/report2.css">
<img src="{YOUR_ABS_PATH}/frontend/statics/img/armoirie_CI.png" alt="afor">
<img src="{YOUR_ABS_PATH}/frontend/statics/img/afor.jpeg" alt="afor">

```

## Run
```
bash create_pdf_report.sh
```
or
```
create_pdf_report.bat
```

## Result
* go to deliverable\
* check report_deliv.html\
* check report.pdf\


## Author
4.0 Team 
