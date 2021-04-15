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

    file_name = 'results.json'
    with open(os.path.abspath(file_name), 'w') as f:
        json.dump(result, f, indent=4)

    return file_name
