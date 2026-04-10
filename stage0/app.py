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
        
        response = requests.get(GENDERIZE_URL, params={"name": name}, timeout=2)

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "Upstream service error"
            }), 502
        
        data = response.json
        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        if gender is None or count  == 0:
            return jsonify({
                "status": "error",
                "message": "No prediction available for the provided name"
            }), 422
        
        sample_size = count
        is_confident = (probability >= 0.7) and (sample_size >= 100)
        
        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
            