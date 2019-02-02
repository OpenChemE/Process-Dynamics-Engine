FROM python:3.7-alpine
RUN apk add --no-cache \
    build-base \
    freetype-dev \
    git \
    openblas-dev
RUN pip install --no-cache-dir -e git+https://github.com/python-control/python-control@601b58152080d89575cc677474ec7714e1a34ee2#egg=control
RUN pip install --no-cache-dir slycot
RUN apk del --no-cache \
    build-base \
    freetype-dev \
    git \
    openblas-dev
