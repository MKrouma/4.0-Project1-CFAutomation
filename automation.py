import os

print("Running automation in docker container ...")
cmd = "cd backend/bash && bash backend.sh"
os.system(cmd)
