# Backend Wizards — Stage 1 API

##  Overview

This project is a Flask-based REST API that generates and stores user profiles by integrating three external services:

* Gender prediction
* Age estimation
* Nationality prediction

It accepts a name, processes it through external APIs, classifies the result, stores it in a database, and exposes endpoints to manage the data.

---

##  Base URL

```
https://your-app.up.railway.app
```

---

##  Tech Stack

* Python (Flask)
* SQLAlchemy (ORM)
* SQLite (development) / PostgreSQL (production-ready)
* Gunicorn (deployment)
* Railway (hosting)

---

## 📦 Features

* Multi-API integration (Genderize, Agify, Nationalize)
* Data persistence with SQLAlchemy
* UUID v7 for unique IDs
* Idempotent profile creation (no duplicates)
* Filtering support (gender, country, age group)
* Proper error handling (400, 422, 404, 502)
* CORS enabled for external access

---

## 📌 Endpoints

### 1. Create Profile

`POST /api/profiles`

**Request:**

```json
{ "name": "ella" }
```

**Response:**

```json
{
  "status": "success",
  "data": { ... }
}
```

If profile exists:

```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { ... }
}
```

---

### 2. Get All Profiles

`GET /api/profiles`

**Optional Query Params:**

* `gender`
* `country_id`
* `age_group`

---

### 3. Get Single Profile

`GET /api/profiles/{id}`

---

### 4. Delete Profile

`DELETE /api/profiles/{id}`

Returns `204 No Content`

---

## 🧠 Classification Rules

* Age Groups:

  * 0–12 → child
  * 13–19 → teenager
  * 20–59 → adult
  * 60+ → senior

* Nationality:

  * Country with highest probability is selected

---

## ⚠️ Error Handling

All errors follow:

```json
{
  "status": "error",
  "message": "..."
}
```

| Code | Description           |
| ---- | --------------------- |
| 400  | Missing or empty name |
| 422  | Invalid type          |
| 404  | Profile not found     |
| 502  | External API failure  |

---

## 🧪 Running Locally

```bash
git clone <repo-url>
cd project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask run
```

---

## 🌍 Deployment

Deployed on Railway using Gunicorn:

```bash
gunicorn app:app
```

---

## 📎 Notes

* All timestamps are in UTC (ISO 8601 format)
* IDs are generated using UUID v7
* Duplicate names return existing records (idempotency)

