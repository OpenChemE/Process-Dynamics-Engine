FROM python:3.7-alpine
RUN apk add --no-cache \
    build-base \
    freetype-dev \
    git \
    openblas-dev
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
RUN apk del --no-cache \
    build-base \
    freetype-dev \
    git \
    openblas-dev
COPY . .
CMD ["python", "server/app.py"]
