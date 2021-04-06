# inaturalist_api
Serves GET requests that will fetch information from iNaturalist, and return the results.

# Requirements
- Python3.9
- Registered application on iNaturalist

# Setup
```python
pip install -r requirements.txt

# Add Callback URL to redirect_uri in the config.json
# Add Application ID to app_id in the config.json
# Add the Secret to app_secret in the config.json
python inaturalist_oauth.py -a          # Generate the access tokens needed by iNaturalist first
python inaturalist_oauth.py -p          # Get the API token from iNaturalist, which will be used in the Authentication header in all the requests
python inaturalist_oauth.py -o > .env   # To print and setup environment variables. You should set these environment variables up in the Heroku app
```

# Usage
To launch this application, run the following command:
```bash
uvicorn main:app --reload
```

To launch this application to Heroku, first set all the necessary environment variables from the config.json in your Heroku deployment. Then 
run the following command:
```bash
git push heroku main
```