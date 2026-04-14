import requests

def get_gender(name):
    res = requests.get(f'https://api.genderize.io?name={name}').json()

    if res.get('gender') is None or res.get('count') == 0:
        raise ValueError('Genderize returned an invalid response')
    
    return res

def get_age(name):
    res = requests.get(f'https://api.agify.io?name={name}').json()

    if res.get('age') is None:
        raise ValueError('Agify returned an invalid response')
    
    return res

def get_nationality(name):
    res = requests.get(f'https://api.nationalize.io?name={name}').json()

    if not res.get('country'): 
        raise ValueError('Nationalize returned an invalid response')
    
    return res