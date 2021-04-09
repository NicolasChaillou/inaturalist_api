import os
import re
import json
import requests
import argparse

import config_helper
from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
config = {}
config_helper.initialize_config(config)


@app.get("/observations")
def get_observations(lng: float, lat: float):
    if not valid_lng_lat(lng, lat):
        return { "err": "Invalid coordinates."}

    headers = {
        "Authentication": config['access_token'],
        "Accept": "application/json"
        }

    q = {
        "geo": "true",
        "identified": "true",
        "mappable": "true",
        "verifiable": "true",
        "identifications": "most_agree",
        "photos": "true",
        "native": "true",
        "lat": lat,
        "lng": lng,
        "radius": 1,
        "page": 1,
        "per_page": 15,
        "order": "desc",
        "order_by": "created_at"
    }
    response = requests.get(f"{config['request_endpoint']}/observations", params=q, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return { "err": f"Error retrieving request: {response.status_code}" }


def valid_lng_lat(lng: float, lat: float):
    if (abs(lng) > 180 or abs(lat) > 90): 
        return False
    return True

@app.get("/refresh")
def refresh_token():
    '''
    This function will request a new access_token, which is needed to make authenticated requests to iNaturalist.
    This access_token expires every 24 hours, so the function should be run at least once a day.
    '''
    headers = { "Authorization": f"Bearer {config['access_token']}" }
    response = requests.get(config["api_token_endpoint"], headers=headers)
    if response.status_code == 200:
        config["api_token"] = response.json()["api_token"]
    else:
        print(f"Failed to fetch new API token. Try refreshing your access token.\n{response}")
