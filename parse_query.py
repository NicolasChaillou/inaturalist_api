import os
import json

def parse_query(response):
    result = {'results': []}
    for p in response['results']:
        result['results'].append({
            'id': p['id'],
            'species_guess': p['species_guess'],
            'longitude': p['geojson']['coordinates'][0],
            'latitude': p['geojson']['coordinates'][1],
            'wiki': p['taxon']['wikipedia_url'],
            'photo': p['taxon']['default_photo']['url']
            })

    return result
