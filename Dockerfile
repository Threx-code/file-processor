ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

#create the virtual environment
RUN python -m venv /opt/venv

#set the virtual environment to current location
ENV PATH=/opt/venv/bin:$PATH

RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#install os dependencies
RUN apt-get update && apt-get install -y \
    #for postgres
    libpq-dev \
    #for pillow
    libjpeg-dev \
    #for cairoSVG
    libcairo2 \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /src
WORKDIR /src

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./src /src
COPY .env .env


ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

ARG PROJECT_NAME="file_processor"


EXPOSE 8000
