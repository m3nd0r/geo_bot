FROM python:3.8.5

RUN pip install --upgrade wheel pip

COPY ./requirements.txt /requirements.txt
RUN pip install -U -r /requirements.txt