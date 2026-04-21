from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app)

    from routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()