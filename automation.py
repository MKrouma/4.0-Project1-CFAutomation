import os

print("Running automation in docker container ...")
cmd = "cd backend/bash && bash create_pdf_report.sh"
os.system(cmd)
