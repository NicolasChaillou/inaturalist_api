import json
import os

# def parse_results(query_file):                                                
def main():
    with open(os.path.abspath('observations.json')) as f:
        info = json.load(f)

    result = {}
    result['results'] = []

    for p in info['results']:
        result['results'].append({
            'id': p['id'],
            'species_guess': p['species_guess'],
            'location': p['location']
            })

    with open(os.path.abspath('results.json'), 'w') as f:
        json.dump(result, f, indent=4)

main()
