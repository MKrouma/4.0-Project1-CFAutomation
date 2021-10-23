# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY . .

# install dependencies
RUN pip install -r requirements_dev.txt
RUN apt-get install libpangocairo-1.0-0

# command to run on container start
CMD pwd
CMD [ "python", "./automation.py" ]