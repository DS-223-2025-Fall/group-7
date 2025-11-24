# Smart Pricing System  
Group 7

**Authors:**  
Arevik Melikyan - PM/PO
Zhanna Balyan - DB Developer
Sona Barseghyan - Backend/API Developer
Edelveys Gevorgyan - Frontend Developer
Elen Ghalechyan — Data Science  


**Created:** ?/11/2025

---

##  Documentation  
Full documentation will be available soon using MkDocs.

---

#  Project Overview  
The **Smart Pricing System** is a microservice-based application designed to automatically determine the optimal product price using **Thompson Sampling (Gaussian)** in real time.

The system includes:

-  **Backend API (Flask)** — users, projects, bandits, experiments, algorithm endpoints  
-  **DS Service** — Gaussian Thompson Sampling implementation  
-  **ETL Service** — initializes database tables  
-  **Frontend (Streamlit)** — dashboard for running pricing experiments  
-  **PostgreSQL Database**  
-  **pgAdmin** for DB administration  

This architecture allows the pricing engine to run in real time and scale independently across services.

---

#  Installation

### 1. Clone repository
```bash
git clone hhttps://github.com/DS-223-2025-Fall/group-7.git
cd smart_pricing
```

### 2. Add `.env`
Create `.env` with:

```
DB_USER=postgres
DB_PASSWORD=admin
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```

### 3. Build & Run Services
```bash
docker compose up --build
```

---

#  Access the Application

After running Docker, access:

###  Streamlit Frontend
**http://localhost:8501**  
Main dashboard for pricing experiments.

###  Backend API (Flask)
**http://localhost:8000**  
Swagger-like description available via endpoints.

###  DS Service
**http://localhost:8888**  
Handles Gaussian Thompson Sampling.

###  pgAdmin (Database GUI)
**http://localhost:5050**  
Login using `.env` credentials.

---

#  Project Structure

```
smart_pricing/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── endpoints.py
│   └── __init__.py
│
├── ds/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── thompson_engine.py
│   ├── service.py
│   └── __init__.py
│
├── etl/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init_db.py
│   └── __init__.py
│
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── assets/
│
├── core/
│   ├── config.py
│   ├── models.py
│   └── __init__.py
│
├── docker-compose.yml
├── .env
└── README.md
```

---

#  ETL

The ETL microservice initializes all database tables.

### Models created:
- **users**
- **projects**
- **bandits**
- **experiments**

Tables are created using:

```python
Base.metadata.create_all(engine)
```

The `etl` container runs **once** at startup, then exits.

---

#  Data Science (Thompson Sampling)

The DS service runs **Gaussian Thompson Sampling** for:

- single project  
- all projects  
- experiment creation (optional)  

Example Gaussian score:

```python
score = random.gauss(mean, sqrt(variance))
```

The DS service communicates directly with the backend via internal Docker networking.

---

#  API (Backend)

The backend provides endpoints for:

### **Authentication**
- `POST /auth/register`
- `POST /auth/login`

### **Projects**
- `POST /projects`
- `GET /projects`
- `PUT /projects/{id}`
- `DELETE /projects/{id}`

### **Bandits**
- `POST /bandits`
- `GET /bandits`
- `GET /bandits/{id}`

### **Experiments**
- `POST /experiments`
- `GET /experiments`

### **Algorithm**
- `POST /algorithm/run/{project_id}`
- `POST /algorithm/run_all`
- `GET /algorithm/optimal_price/{project_id}`

The backend defaults to:

```
strategy="gaussian"
```

---

# Docker Services

### Database
```yaml
db:
  image: postgres:16
  ports:
    - "5432:5432"
```

### pgAdmin
```yaml
pgadmin:
  image: dpage/pgadmin4
  ports:
    - "5050:80"
```

### Backend
```yaml
backend:
  build:
    context: .
    dockerfile: backend/Dockerfile
  ports:
    - "8000:8000"
```

### DS
```yaml
ds:
  build:
    context: .
    dockerfile: ds/Dockerfile
  ports:
    - "8888:8888"
```

### ETL
```yaml
etl:
  build:
    context: .
    dockerfile: etl/Dockerfile
  restart: "no"
```

### Frontend
```yaml
frontend:
  build:
    context: .
    dockerfile: frontend/Dockerfile
  ports:
    - "8501:8501"
```

---

#  Web Application (Streamlit)

The main dashboard allows you to:

- Authenticate  
- Add new products  
- Choose price variants  
- Run Thompson Sampling  
- View experiment stats  
- Monitor bandits  
- Display conversion rates  
- See suggested optimal price  

Frontend communicates with backend at:

```
http://backend:8000
```

---

#  How to Use the System

### 1. Register & Login  
Create an account in the Streamlit GUI.

### 2. Create Product  
Enter product name + price variants.

### 3. Start Experiment  
System will run Gaussian TS immediately.

### 4. View Results  
See conversion, allocation, rewards.

### 5. Inspect DB  
Use pgAdmin for monitoring data.


---

#  Contributors

Group 7 — Smart Pricing System, American University of Armenia  
Fall 2025.

---

