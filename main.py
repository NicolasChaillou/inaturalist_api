import os
import re
import json
import requests
import argparse

from parse_query import parse_query
from config import initialize_config
from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
config = {}
initialize_config(config)


@app.get("/observations")
def get_observations(lng: float, lat: float):
    headers = {"Authentication": config['access_token']}
    
    query = {
        "captive": "false",
        "endemic": "true",
        "geo": "true",
        "identified": "true",
        "mappable": "true",
        "native": "true",
        "photos": "true",
        "identifications": "most_agree",
        "lat": lat,
        "lng": lng,
        "radius": 5,
        "page": 1,
        "per_page": 15,
        "order": "desc",
        "order_by": "created_at"
    }

    
    response = requests.get(f"{config['request_endpoint']}/observations", params=query, headers=headers)
    
    if response.status_code == 200:
        return parse_query(response.json())
    else:
        print(f"Failed request: {response}")


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
