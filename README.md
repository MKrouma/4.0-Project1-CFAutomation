# 4.0-Team
Project to automate map production for PAMOFOR.

## Project content
* Backend 
* Database
* Deliverable
* Frontend 

## Table of content
* How to run
* Run 
* Result
* Author

## How to run
### Clone project
Clone project and go later to project folder.
```
git clone https://github.com/MKrouma/4.0-Project1-CFAutomation.git
```
```
cd 4.0-Project1-CFAutomation
```


### Create a virtual environment
```
python -m venv env
```

### Activate virtual environment with 
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

### Create new git branch
```
git checkout -b {YOUR_NAME}_dev_branch
```

### Change manually some stuff
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
or (for Windows users)
```
create_pdf_report.bat
```

## Result
Go to deliverable folder
* check report_deliv.html
* check report.pdf


## Author
4.0 Team 
