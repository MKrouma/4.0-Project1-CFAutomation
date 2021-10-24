# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /workspace

# copy the dependencies file to the working directory
COPY . .

# install dependencies
RUN pip install -r requirements_dev.txt
RUN apt-get install libpangocairo-1.0-0
RUN apt install python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
