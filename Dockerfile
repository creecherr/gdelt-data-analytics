# this is an official Python runtime, used as the parent image
FROM python:3.7-stretch

LABEL maintainer="Haley Creech <haley.creech@gmail.com>"

WORKDIR /gdelt-data-analytics-service/

ADD . /gdelt-data-analytics-service/

RUN pip install -r requirements.txt

# execute the Flask app
CMD ["python3", "app.py"]