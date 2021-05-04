# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY NAFA.py NAFAUser.py testController.py graphs .

CMD["python3", "testController.py"]