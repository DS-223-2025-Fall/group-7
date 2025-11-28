# Dockerfile
FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY backend/requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /backend/requirements.txt

COPY backend /backend

EXPOSE 8000

CMD ["uvicorn", "endpoints:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
