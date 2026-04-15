from flask import request, jsonify
from extensions  import db
from models import Profile
from services import *
from utils import *
from uuid6 import uuid7
from datetime import datetime

def register_routes(app):
    @app.route('/api/profiles', methods=['POST'])
    def create_profile():
        data = request.get_json()

        if not data or 'name' not in data:
            return jsonify({'status':'error', 'message':'Missing or emptyname'}), 400    
        
        name = data['name']

        if not isinstance (name,str):
            return jsonify({'status':'error', 'message':'Invalid type'}), 422
        
        name = name.lower().strip()

        existing_profile = Profile.query.filter_by(name=name).first()

        if existing_profile:
            return jsonify({
                'status':'success',
                'message':'Profile already exists',
                'data': serialize(existing_profile)
                }), 200
        
        try:
            gender = get_gender(name)
            age = get_age(name)
            nat = get_nationality(name)
        except ValueError as e:
            return jsonify({'status':'error', 'message':str(e)}), 502   

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

        db.session.add(profile)
        db.session.commit()

        return jsonify({
            'status':'success',
            'data': serialize(profile)  
        }), 201

    @app.route('/api/profiles/<id>', methods=['GET'])
    def get_profile(id):
        profile = Profile.query.get(id)

        if not profile:
            return jsonify({'status':'error', 'message':'Profile not found'}), 404
        
        return jsonify({
            'status':'success',
            'data': serialize(profile)
        }), 200
    
    @app.route('/api/profiles', methods=['GET'])
    def get_profiles():
       gender = request.args.get('gender')
       country_id = request.args.get('country_id')
       age_group = request.args.get('age_group')

       query = Profile.query

       if gender:
           query = query.filter(Profile.gender.ilike(gender))
       if country_id:
           query = query.filter(Profile.country_id.ilike(country_id))
       if age_group:
           query = query.filter(Profile.age_group.ilike(age_group))

       results = query.all()
       return jsonify({
           'status':'success',
           'count': len(results),
           'data': [minimal(p) for p in results]
         }), 200
    
    @app.route('/api/profiles/<id>', methods=['DELETE'])
    def delete_profile(id):
        profile = Profile.query.get(id)

        if not profile:
            return jsonify({'status':'error', 'message':'Profile not found'}), 404
        
        db.session.delete(profile)
        db.session.commit()

        return '', 204
    
def serialize(p): 
    return {
        'id': p.id,
        'name': p.name,
        'gender': p.gender,
        'gender_probability': p.gender_probability,
        'sample_size': p.sample_size,
        'age': p.age,
        'age_group': p.age_group,
        'country_id': p.country_id,
        'country_probability': p.country_probability,
        'created_at': p.created_at.isoformat() + 'Z'
    }

def minimal(p):
    return {
        'id': p.id,
        'name': p.name,
        'gender': p.gender,
        'age': p.age,
        'age_group': p.age_group,
        'country_id': p.country_id,
    }

          


        