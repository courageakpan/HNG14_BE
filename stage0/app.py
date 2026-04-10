from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone

app = Flask(__name__)
GENDERIZE_URL = "https://api.genderize.io"

@app.route("/api/classify", methods=["GET"])
def classify():
    name = request.args.get("name")
    if name is None or name.strip() == "":
        return jsonify({
           "status": "error",
           "message": "Missing or empty name paremeter"
            }), 400
    
    if not isinstance(name, str):
        return jsonify({
           "status": "error",
           "message": "Name parameter must be a string"
            }), 422
    
    try:
        
        response = requests.get(GENDERIZE_URL, params={"name": name}, timeout=5)

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "Upstream service error"
            }), 502
        
        data = response.json()
        gender = data.get("gender")
        probability = float(data.get("probability", 0))
        count = data.get("count")

        if not gender or count == 0 or count < 5:
            return jsonify({
                "status": "error",
                "message": "No prediction available for the provided name"
            }), 422
        
        sample_size = count
        is_confident = (probability >= 0.7) and (sample_size >= 100)
        
        processed_at = datetime.now(timezone.utc)\
                    .replace(microsecond=0)\
                    .isoformat()\
                    .replace("+00:00", "Z")
                    

        return jsonify({
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }), 200
    except requests.exceptions.RequestException:
        return jsonify({
            "status": "error",
            "message": "Failed to connect to external service"
        }), 500
    
    except Exception:
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)    

            