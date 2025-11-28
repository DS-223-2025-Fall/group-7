FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# shared core
COPY core /app/core
# backend service
COPY backend /app/backend

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "-m", "backend.main"]
