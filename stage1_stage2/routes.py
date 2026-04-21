from flask import app, request, jsonify
from extensions import db
from models import Profile
from services import get_gender, get_age, get_nationality
from utils import get_age_group, get_top_country, parse_query, serialize, minimal
from uuid6 import uuid7
from datetime import datetime
from sqlalchemy import func


def register_routes(app):

    @app.route('/ping')
    def ping():
        return "STAGE 2 NEW CODE LIVE"

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

        existing_profile = Profile.query.filter(
            func.lower(Profile.name) == name
        ).first()

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

    @app.route('/api/profiles', methods=['GET'])
    def get_profiles():
        try:
            query = Profile.query

            # FILTERS
            gender = request.args.get('gender')
            age_group = request.args.get('age_group')
            country_id = request.args.get('country_id')
            min_age = request.args.get('min_age')
            max_age = request.args.get('max_age')
            min_gender_probability = request.args.get('min_gender_probability')
            min_country_probability = request.args.get('min_country_probability')

            if gender:
                query = query.filter(func.lower(Profile.gender) == gender.lower())

            if age_group:
                query = query.filter(func.lower(Profile.age_group) == age_group.lower())

            if country_id:
                query = query.filter(func.lower(Profile.country_id) == country_id.lower())

            if min_age:
                query = query.filter(Profile.age >= int(min_age))

            if max_age:
                query = query.filter(Profile.age <= int(max_age))

            if min_gender_probability:
                query = query.filter(Profile.gender_probability >= float(min_gender_probability))

            if min_country_probability:
                query = query.filter(Profile.country_probability >= float(min_country_probability))

            # SORTING
            sort_by = request.args.get('sort_by')
            order = request.args.get('order', 'asc')

            if sort_by:
                column = getattr(Profile, sort_by, None)
                if not column:
                    return jsonify({"status": "error", "message": "Invalid query parameters"}), 400

                if order == 'desc':
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column.asc())

            # PAGINATION
            page = int(request.args.get('page', 1))
            limit = min(int(request.args.get('limit', 10)), 50)

            offset = (page - 1) * limit

            total = query.count()

            results = query.offset(offset).limit(limit).all()

            return jsonify({
                "status": "success",
                "page": page,
                "limit": limit,
                "total": total,
                "data": [serialize(p) for p in results]
            }), 200

        except:
            return jsonify({"status": "error", "message": "Invalid query parameters"}), 400

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
    
    @app.route('/api/profiles/search', methods=['GET'])
    def search_profiles():
        q = request.args.get('q')

        if not q:
            return jsonify({
                "status": "error",
                "message": "Missing or empty parameter"
            }), 400

        filters = parse_query(q)

        if not filters:
            return jsonify({
                "status": "error",
                "message": "Unable to interpret query"
            }), 400

        query = Profile.query

        if "gender" in filters:
            query = query.filter(Profile.gender == filters["gender"])

        if "age_group" in filters:
            query = query.filter(Profile.age_group == filters["age_group"])

        if "country_id" in filters:
            query = query.filter(Profile.country_id == filters["country_id"])

        if "min_age" in filters:
            query = query.filter(Profile.age >= filters["min_age"])

        if "max_age" in filters:
            query = query.filter(Profile.age <= filters["max_age"])

        # Pagination
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 10)), 50)

        offset = (page - 1) * limit
        total = query.count()

        results = query.offset(offset).limit(limit).all()

        return jsonify({
            "status": "success",
            "page": page,
            "limit": limit,
            "total": total,
            "data": [serialize(p) for p in results]
        }), 200