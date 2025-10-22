# String Analyzer Service – FastAPI  
HNG Internship Stage 1 Task – Backend (Python, FastAPI, SQLite)

---

## 📖 Overview
This project is my **Stage 1 Backend Task** for the HNG Internship.  

It is a RESTful API built with **FastAPI** that:
- Analyzes strings
- Computes and stores their properties
- Allows filtering via query parameters
- Supports **natural language queries** (basic parsing)
- Provides CRUD-like operations for managing strings

---

## 👤 Author
- **Name:** Jesse Onoyeyan 
- **Email:** jesseonoyeyan@gmail.com 
- **Stack:** Python (FastAPI)

---

## ⚡ Features
- **POST /strings** → Analyze and store a string  
- **GET /strings/{string_value}** → Retrieve a specific string  
- **GET /strings** → Filter by length, palindrome, word count, etc.  
- **GET /strings/filter-by-natural-language** → Filter using natural language queries  
- **DELETE /strings/{string_value}** → Delete a string  

---

## 🛠 Tech Stack
- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy + SQLite**
- **Pydantic v2**
- **Pytest** (for testing)

---

## 🔑 Environment Variables

This project uses environment variables from a `.env` file.

### `.env.example`
Committed to the repo to show required variables:
```env
# Environment variables
# Database connection string
DATABASE_URL=sqlite:///./strings.db

# Optional app metadata
APP_NAME=String Analyzer API
DEBUG=True
```
---
## ⚙️ Setup (Local Development)
**Clone Repo**
```bash
git clone git@github.com:lordpacificsmartly/hng-stage1-string-analyzer.git
cd hng-stage1-string-analyzer
```
**Create Virtual Environment & Install Dependencies**
```base
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
---
**Run the API**
```bash
uvicorn app.main:app --reload --port 8000
```
---
**🧪 Running Tests**
```bash
python -m pytest -q
```