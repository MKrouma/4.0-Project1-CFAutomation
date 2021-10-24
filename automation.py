import os

print("Running automation in docker python env !")
# os
# OS_ENV = os.getenv(["OS"])
OS_ENV = "Mac" # to-automate

# cmd create report
cmd = None
if OS_ENV == "Linux" or OS_ENV == "Mac" :
    cmd = "cd backend/bash && bash create_pdf_report.sh"
    os.system(cmd)

if OS_ENV == "Windows" :
    cmd = "cd backend\bash && create_pdf_report.bat"
    os.system(cmd)