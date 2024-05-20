# syntax=docker/dockerfile:1
FROM python:3.12.2

COPY requirements.txt /tmp/requirements.txt
COPY docker/jupyter/requirements.txt /tmp/docker/jupyter/requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache \
    pip install -r /tmp/requirements.txt

WORKDIR /code

ADD script.py ./

CMD [ "python", "script.py" ]
