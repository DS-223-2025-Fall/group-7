import requests
import os

API_BASE = os.getenv("BACKEND_URL", "http://backend:8000")

def fetch_projects():
    r = requests.get(f"{API_BASE}/projects")
    return r.json()

def create_project(name, n_bandits, initial_price):
    r = requests.post(f"{API_BASE}/projects", json={
        "description": name,
        "number_bandits": n_bandits,
        "price": initial_price
    })
    return r.json()

def upload_project_image(pid, file):
    files = {"file": (file.name, file, file.type)}
    requests.post(f"{API_BASE}/projects/{pid}/upload-image", files=files)

def create_bandit(pid, price):
    requests.post(f"{API_BASE}/projects/{pid}/bandits", json={"price": price})

def fetch_bandits(pid):
    r = requests.get(f"{API_BASE}/projects/{pid}/bandits")
    return r.json()

def fetch_posterior_plot(pid):
    r = requests.get(f"{API_BASE}/projects/{pid}/thompson/plot")
    if r.status_code == 200:
        return r.content
    return None
