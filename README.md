# 4.0-Team
Project to automate map production for PAMOFOR.

## Table of content
* Installation
* Development
* Collaboration


## Installation
### clone project
Clone project and go later to project folder.
```
git clone https://github.com/MKrouma/4.0-Project1-CFAutomation.git
```
```
cd 4.0-Project1-CFAutomation
```

### build docker image
install docker, run docker daemon
```
docker build -t 40team .
```

### run container
```
docker run -p 8888:80 -it -v deliverable:/workspace/deliverable 40team
docker run -p 8888:80 -it -v deliverable:/workspace/deliverable 40team /bin/bash
```


## Development
### configurations
change project directory & module path
```
PROJECT_PATH = /Users/mac/Desktop/4.0-Project1-CFAutomation
MODULE_PATH = "/Users/mac/Desktop/4.0-Project1-CFAutomation/backend/module"
```

### virtual env
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
```

### run automation
`In container terminal :`
```
python3 automation.py
```

### results
`In local terminal :`
```
docker cp {CONTAINER_ID}:/workspace/deliverable .
```
`Subset : find container id with : docker container ls`

Go to deliverable folder : 
* check report_deliv.html
* check report.pdf


## Collaboration (git & github)
### create new branch 
`In local terminal :`
```
git checkout -b {ISSUE_NUMBER}_{YOURNAME}_{Others}
```
### do your development
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

### summit a pull request (PR)
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

### share information
* something to share ?\
```
Something interesting ? A stackoverflow solution or otehrs ?
In references.txt, put description and solution link.

Exemple :
---------
Description : code to run mapbox api without paying too much
soluion : http://xxxxxxx.com?xxxxx
```


## Backend process
> create directories (*shapefile*) \
> create boundaries (*field*) \
> set map configurations (*field*) \
> render static map (*field*) \
> render html for (*field*) \
> trnasform html to pdf (*field*)

