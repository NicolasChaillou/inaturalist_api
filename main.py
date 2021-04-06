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
except Exception as err:
    print("Problem getting environment variables.")
    exit()

print(f"Config: {config}")

@app.get("/observations")
def get_observations(long: float, lat: float):
    pass

