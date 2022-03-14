# NOTE: This is a copy and edited version from the following content
# REF: https://dev.to/googlecloud/using-headless-chrome-with-cloud-run-3fdp
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# Install manually all the missing libraries
RUN apt-get update
# RUN apt update && apt install -y zip htop screen libgl1-mesa-glx fonts-liberation

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app

CMD python ./main.py

