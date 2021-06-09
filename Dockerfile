FROM python:3.8

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt config.py .env ./
COPY app app

RUN apt-get upgrade
RUN apt update
RUN apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx


RUN pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt 
RUN pip install -r requirements.txt
RUN pip install torch
RUN pip install imgaug
RUN pip install tensorflow==2.4.0
RUN pip install keras==2.4.3


EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
