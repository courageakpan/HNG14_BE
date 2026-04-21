from datetime import timezone


def get_age_group(age):
    if age <= 12:
        return 'child'
    elif age <= 19:
        return 'teenager'
    elif age <= 59:
        return 'adult'
    return 'senior'

def get_top_country(countries):
    return max(countries, key=lambda x: x['probability'])

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
        'created_at': (
            p.created_at
            .replace(tzinfo=timezone.utc)
            .replace(microsecond=0)
            .isoformat() 
            .replace('+00:00', 'Z')
        )
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

def parse_query(q):
    q = q.lower()
    filters = {}

    if "male" in q:
        filters["gender"] = "male"
    if "female" in q:
        filters["gender"] = "female"

    if "adult" in q:
        filters["age_group"] = "adult"
    if "teenager" in q:
        filters["age_group"] = "teenager"
    if "child" in q:
        filters["age_group"] = "child"
    if "senior" in q:
        filters["age_group"] = "senior"

    if "young" in q:
        filters["min_age"] = 16
        filters["max_age"] = 24

    import re
    match = re.search(r'above (\d+)', q)
    if match:
        filters["min_age"] = int(match.group(1))

    countries = {
        "nigeria": "NG",
        "kenya": "KE",
        "angola": "AO"
    }

    for key in countries:
        if key in q:
            filters["country_id"] = countries[key]

    return filters if filters else None