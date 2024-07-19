FROM python:3.8.1

WORKDIR /app/src/

COPY ./requirements.txt .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


RUN pip install -r requirements.txt

