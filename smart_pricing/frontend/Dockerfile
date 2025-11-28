FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /frontend

COPY frontend/requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend /frontend

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true", "--server.runOnSave=true"] 