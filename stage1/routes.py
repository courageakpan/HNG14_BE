from flask import request, jsonify
from extensions import db
from models import Profile
from services import *
from utils import *
from uuid6 import uuid7
from datetime import datetime
from sqlalchemy import func


def register_routes(app):

    @app.route('/api/profiles', methods=['POST'])
    def create_profile():
        data = request.get_json(silent=True)

        if not data or 'name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing or empty name'
            }), 400

        name = data.get('name')

        if not isinstance(name, str):
            return jsonify({
                'status': 'error',
                'message': 'Invalid type'
            }), 422

        if not name.strip():
            return jsonify({
                'status': 'error',
                'message': 'Missing or empty name'
            }), 400

        name = name.lower().strip()

        existing_profile = Profile.query.filter_by(name=name).first()

        if existing_profile:
            return jsonify({
                'status': 'success',
                'message': 'Profile already exists',
                'data': serialize(existing_profile)
            }), 200

        try:
            gender = get_gender(name)
            age = get_age(name)
            nat = get_nationality(name)
        except ValueError as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 502

        age_group = get_age_group(age['age'])
        top_country = get_top_country(nat['country'])

        profile = Profile(
            id=str(uuid7()),
            name=name,
            gender=gender["gender"],
            gender_probability=gender["probability"],
            sample_size=gender["count"],
            age=age["age"],
            age_group=age_group,
            country_id=top_country["country_id"],
            country_probability=top_country["probability"],
            created_at=datetime.utcnow()
        )

        try:
            db.session.add(profile)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500

        return jsonify({
            'status': 'success',
            'data': serialize(profile)
        }), 201


    @app.route('/api/profiles/<id>', methods=['GET'])
    def get_profile(id):
        profile = db.session.get(Profile, id)

        if not profile:
            return jsonify({
                'status': 'error',
                'message': 'Profile not found'
            }), 404

        return jsonify({
            'status': 'success',
            'data': serialize(profile)
        }), 200


    @app.route('/api/profiles', methods=['GET'])
    def get_profiles():
        gender = request.args.get('gender')
        country_id = request.args.get('country_id')
        age_group = request.args.get('age_group')

        query = Profile.query

        if gender:
            query = query.filter(func.lower(Profile.gender) == gender.lower())

        if country_id:
            query = query.filter(func.lower(Profile.country_id) == country_id.lower())

        if age_group:
            query = query.filter(func.lower(Profile.age_group) == age_group.lower())

        results = query.all()

        return jsonify({
            'status': 'success',
            'count': len(results),
            'data': [minimal(p) for p in results]
        }), 200


    @app.route('/api/profiles/<id>', methods=['DELETE'])
    def delete_profile(id):
        profile = db.session.get(Profile, id)

        if not profile:
            return jsonify({
                'status': 'error',
                'message': 'Profile not found'
            }), 404

        db.session.delete(profile)
        db.session.commit()

        return '', 204