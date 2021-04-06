import os
import re
import json
import requests
import  argparse

from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

config = {}
try:
    config["site"] = str(os.getenv("site"))
    config["api_token"] = str(os.getenv("api_token"))
    config["api_token_endpoint"] = str(os.getenv("api_token_endpoint"))
    config["access_token"] = str(os.getenv("access_token"))
    config["app_id"] = str(os.getenv("app_id"))
    config["app_secret"] = str(os.getenv("app_secret"))
    config["redirect_uri"] = str(os.getenv("redirect_uri"))
    config["created_at"] = int(os.getenv("created_at"))
    config["request_endpoint"] = str(os.getenv("request_endpoint"))
except Exception as err:
    print("Problem getting environment variables.")
    exit()


app = FastAPI()

@app.get("/observations")
def get_observations(long: float, lat: float):
    headers = {"Authentication": config['access_token']}
    response = requests.get(f"{config['request_endpoint']}/users/your_user_here", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed request: {response}")

