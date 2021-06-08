FROM python:3.6

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt config.py .env ./
COPY app app

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

RUN pip install -r requirements.txt

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
