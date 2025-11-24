FROM python:3.11-slim

WORKDIR /app

COPY etl/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY core /app/core
COPY etl /app/etl

ENV PYTHONPATH=/app

CMD ["python", "-m", "etl.init_db"]
