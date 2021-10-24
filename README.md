# 4.0-Team
Project to automate map production for PAMOFOR.

## Table of content
* Run
* Manual
* Development


## Run
### Clone project
Clone project and go later to project folder.
```
git clone https://github.com/MKrouma/4.0-Project1-CFAutomation.git
```
```
cd 4.0-Project1-CFAutomation
```

### build docker image
```
docker build -t 40team .
```

### Run docker image bash
```
docker run -p 8888:8888 -it -v deliverable:/deliverable 40team /bin/bash
```

## Manual
* go the html file `frontend/templates/report_{YOUR_OS}.html`
* change css, armoirie-logo, afor-logo and g-tec path
```
<link rel="stylesheet" href="{YOUR_ABS_PATH}/frontend/statics/css/report.css">
<img src="{YOUR_ABS_PATH}/frontend/statics/img/armoirie_CI.png" alt="afor">
<img src="{YOUR_ABS_PATH}/frontend/statics/img/afor.jpeg" alt="afor">
<img src="{YOUR_ABS_PATH}\frontend\statics\img\g-tec.png" alt="afor">
```


## Development
### run bash code
`In container terminal :`
```
cd backend/bash
bash create_pdf_report.sh
```

### Check
Go to deliverable folder : 
* check report_deliv.html
* check report.pdf


### Collaboration (Git & Github)
* Create new branch \
`In container terminal :`
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

* Pull request and add Mamadou for assignment \
`Go to Github, Pull request and create a new one`

* close an issue
```
git commit -m "{YOUR_NAME} {ISSUE} {EXPLAIN} {STATUS} closed #{ISSUE_NUMBER}"
```

* delete branch local & remote (ànly after a PR)
```
git branch -D {ISSUE_NUMBER}_{YOURNAME}_{Others}
git push origin --delete {ISSUE_NUMBER}_{YOURNAME}_{Others}
```

* something to share ?\
`Something interesting ? A stackoverflow solution or otehrs ?`\
`In references.txt, put description and solution  link.`