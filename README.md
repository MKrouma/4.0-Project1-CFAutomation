# 4.0-Team
Project to automate map production for PAMOFOR.

## Table of content
* Installation (Linux-Mac)
* Installation (Windows)
* Collaboration (Git & Github)

## Installation (Linux-Mac)
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

### Activate virtual environment 
```
source env/bin/activate
```

### Install requirements
```
pip install -r requirements_dev.txt
```

### Change manually some stuff
* go the html file `frontend/templates/report_{YOUR_OS}.html`
* change css, armoirie-logo, afor-logo and g-tec path
```
<link rel="stylesheet" href="{YOUR_ABS_PATH}/frontend/statics/css/report.css">
<img src="{YOUR_ABS_PATH}/frontend/statics/img/armoirie_CI.png" alt="afor">
<img src="{YOUR_ABS_PATH}/frontend/statics/img/afor.jpeg" alt="afor">
<img src="{YOUR_ABS_PATH}\frontend\statics\img\g-tec.png" alt="afor">
```

### Run project 
```
bash create_pdf_report.sh
```

### Verify results
Go to deliverable folder : 
* check report_deliv.html
* check report.pdf

## Installation (Windows)
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

### Activate virtual environment 
```
env/Scripts/activate
```

### Install requirements
```
pip install pipwin
```
```
pipwin install gdal, fiona, geopandas, rasterio, shapely
```
```
pip install weasyprint
```

### Change manually some stuff
* go the html file `frontend/templates/report_{YOUR_OS}.html`
* change css, armoirie-logo, afor-logo and g-tec path
```
<link rel="stylesheet" href="{YOUR_ABS_PATH}\frontend\statics\css\report.css">
<img src="{YOUR_ABS_PATH}\frontend\statics\img\armoirie_CI.png" alt="afor">
<img src="{YOUR_ABS_PATH}\frontend\statics\img\afor.jpeg" alt="afor">
<img src="{YOUR_ABS_PATH}\frontend\statics\img\g-tec.png" alt="afor">
```

### Run project 
```
create_pdf_report.bat
```

### Verify results
Go to deliverable folder : 
* check report_deliv.html
* check report.pdf

## Collaboration (Git & Github)
* Choose an issue in Github and create a new branch for each issue;
```
git checkout -b {ISSUE_NUMBER}_{YOURNAME}_{Others}
```
* Do your development;
* Add, commit and push your stuff
```
git add file (or .)
```
```
git commit -m "{YOUR_NAME} {ISSUE} {EXPLAIN} {STATUS}"
```
```
git push origin {ISSUE_NUMBER}_{YOURNAME}_{Others}
```

* Pull request and add Mamadou for assignment
`Go to Github, Pull request and create a new one`

* close an issue
```
git commit -m "{YOUR_NAME} {ISSUE} {EXPLAIN} {STATUS} closed #{ISSUE_NUMBER}"
```