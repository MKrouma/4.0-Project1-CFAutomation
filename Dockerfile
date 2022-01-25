# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /workspace

# copy the dependencies file to the working directory
COPY . .

# install dependencies
RUN pip install -r requirements.txt
RUN apt-get install libpangocairo-1.0-0

# install nodejs, npm and simplify-geojson
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - 
#RUN apt-get install -y nodejs
RUN apt-get install nodejs
RUN npm install -g simplify-geojson

# Docker expose port
EXPOSE 80

# command to run on container start
CMD [ "python", "./automation.py" ]
