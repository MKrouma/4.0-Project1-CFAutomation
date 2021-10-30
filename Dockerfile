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
RUN apt install curl
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN npm install -g simplify-geojson

EXPOSE 80

# command to run on container start
CMD pwd
CMD [ "python", "./automation.py" ]
