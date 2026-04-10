from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone

app = Flask(__name__)
GENDERIZE_URL = "https://api.genderize.io"