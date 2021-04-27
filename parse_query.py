import os
import json

def parse_query(response):
    with open(response) as f:
        info = json.load(f)

    result = {}
    result['results'] = []

    for p in info['results']:
        result['results'].append({
            'id': p['id'],
            'species_guess': p['species_guess'],
            'location': p['location']
            })

    return result
