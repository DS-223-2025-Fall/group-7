FROM python:3.11-slim

WORKDIR /app

COPY ds/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY core /app/core
COPY ds /app/ds

ENV PYTHONPATH=/app

EXPOSE 8888

CMD ["python", "-m", "ds.service"]
