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