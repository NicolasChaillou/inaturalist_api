import os
import re
import json
import time
import threading
import requests
import argparse

from parse_query import parse_query
from config_helper import initialize_config
from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
config = {}
initialize_config(config)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://pokinaturalists.herokuapp.com/",
    "https://pokinaturalists.herokuapp.com:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

def refresh_token():
    '''
    This function will request a new access_token, which is needed to make authenticated requests to iNaturalist.
    This access_token expires every 24 hours, so the function should be run at least once a day.
    '''
    while True:
        time.sleep(36000)
        headers = { "Authorization": f"Bearer {config['access_token']}" }
        response = requests.get(config["api_token_endpoint"], headers=headers)
        if response.status_code == 200:
            config["api_token"] = response.json()["api_token"]
            print("Received new api_token")
        else:
            print("Failed to get new API token")

refresh_thread = threading.Thread(target=refresh_token, daemon=True)
refresh_thread.start()


@app.get("/observations")
def get_observations(lng: float, lat: float):
    '''
    Send Authenticated query to iNaturalist to retrieve observations within
    a radius around the user's longitude and latitude.
    '''
    if not valid_lng_lat(lng, lat):
        return { "err": "Invalid coordinates."}

    headers = {
        "Authentication": config['access_token'],
        "Accept": "application/json"
        }

    query = {
        "captive": "false",
        "endemic": "true",
        "geo": "true",
        "identified": "true",
        "mappable": "true",
        "verifiable": "true",
        "identifications": "most_agree",
        "photos": "true",
        "native": "true",
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
        return { "err": f"Error retrieving request: {response.status_code}" }


def valid_lng_lat(lng: float, lat: float):
    '''
    Validate longitude and latitude from incoming request.
    '''
    if (abs(lng) > 180 or abs(lat) > 90): 
        return False
    return True
