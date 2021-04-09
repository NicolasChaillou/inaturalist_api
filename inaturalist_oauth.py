import re
import json
import requests
import  argparse

from config_helper import print_config_as_env

# NOTE: API Tokens expire after 24 hours. You can request another with the access token you generate with this script.

code_regex = re.compile(r"code=(\w+)")


def load_config():
    try:
        with open("config.json") as f:
            config = json.load(f)
        return config
    except IOError as err:
        print("Config not found")
        exit()

def request_auth_code(config):
    url = f"{config['site']}/oauth/authorize?client_id={config['app_id']}&redirect_uri={config['redirect_uri']}&response_type=code"
    print(f"Click this link to approve this request:\n{url}")

    redirect_uri = input(f"\n\nPlease enter the full redirect link: ")
    if code := code_regex.search(redirect_uri):
        auth_code = code.group(1)
    return auth_code

def request_auth_token(config, auth_code):
    url = f"{config['site']}/oauth/authorize?client_id={config['app_id']}&redirect_uri={config['redirect_uri']}&response_type=code"
    payload = {
        "client_id": config['app_id'],
        "client_secret": config['app_secret'],
        "code": auth_code,
        "redirect_uri": config['redirect_uri'],
        "grant_type": "authorization_code"
    }
    response = requests.post(f"{config['site']}/oauth/token", data=payload)
    if response.status_code == 200:
        return response.json()
    print(f"Did not get 200 back.\n{response.json()}")

def update_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def generate_access_token(config):
    auth_code = request_auth_code(config)
    token_response = request_auth_token(config, auth_code)
    config["access_token"] = token_response["access_token"]
    config["created_at"] = token_response["created_at"]
    update_config(config)

def refresh_api_token(config):
    headers = { "Authorization": f"Bearer {config['access_token']}" }
    response = requests.get(config["api_token_endpoint"], headers=headers)
    if response.status_code == 200:
        config["api_token"] = response.json()["api_token"]
        update_config(config)
    else:
        print(f"Failed to fetch new API token. Try refreshing your access token.\n{response}")

def main():
    parser = argparse.ArgumentParser(description="Setup authentication for inaturalist API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--auth", "-a", action="store_true", help="Generate access token")
    group.add_argument("--api", "-p", action="store_true", help="Fetch new API token")
    group.add_argument("--output", "-o", action="store_true", help="Print out config in .env format")
    args = parser.parse_args()

    config = load_config()
    if args.auth: generate_access_token(config)
    elif args.api: refresh_api_token(config)
    elif args.output: print_config_as_env(config)

main()