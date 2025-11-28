FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*
    

WORKDIR /core

COPY core/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY core /core

CMD ["python", "-m", "init_db"]