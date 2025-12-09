# API Models — Smart Pricing Playground

This document lists the main request and response models used in the backend API.  
Models are implemented using Pydantic (FastAPI) and define the structure, validation rules, and semantics of API payloads.

---

## 1. Project Models

### **ProjectCreate**
Used when creating a new product.

```python
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    image_path: str | None = None
