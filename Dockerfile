FROM 473362459196.dkr.ecr.us-west-2.amazonaws.com/python:latest

RUN pip3.8 install django djangorestframework-jsonapi psycopg2-binary spacy
RUN pip3.8 install "urllib3<2"
RUN python3 -m spacy download en_core_web_sm
