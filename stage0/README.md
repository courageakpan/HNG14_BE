# HNG Stage 0 Backend API

A simple REST API that classifies a name by gender using the Genderize.io API and returns a processed response.

---


##  Endpoint

### 1. Classify Name

**GET** `/api/classify?name={name}`

#### ✅ Success Response (200)

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```

---

##  Processing Logic

* Fetch data from **Genderize API**
* Extract:

  * `gender`
  * `probability`
  * `count` → renamed to `sample_size`
* Compute:

  * `is_confident = true` when:

    * `probability >= 0.7`
    * `sample_size >= 100`
* Generate:

  * `processed_at` (UTC, ISO 8601 format)

---

##  Error Handling

### 400 Bad Request

```json
{
  "status": "error",
  "message": "Missing or empty name parameter"
}
```

### 422 Unprocessable Entity

```json
{
  "status": "error",
  "message": "Name parameter must be a string"
}
```

OR

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

### 500 / 502 Server Errors

```json
{
  "status": "error",
  "message": "Failed to connect to external service"
}
```

---

##  Testing

You can test using:

### Browser

```
https://hng.up.railway.app/api/classify?name=john
```

### Postman

* Method: GET
* URL: `/api/classify?name=john`

---

##  Tech Stack

* Python
* Flask
* Requests
* Gunicorn (for production)
* Railway (deployment)

---

##  Project Structure

```
stage0/
│── app.py
│── requirements.txt
│── Procfile
```

---

## ▶️ Running Locally

1. Clone the repo:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo/stage0
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run app:

```bash
python app.py
```

---

##  CORS

CORS is enabled:

```
Access-Control-Allow-Origin: *
```

---
