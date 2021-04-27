# inaturalist_api
Authenticated server that serves GET requests to the requester with observation information from iNaturalist.

# Requirements
- Python 3.9
- Registered application on iNaturalist
- Running on Linux machine (if running locally)

# Setup
```python
pip install -r requirements.txt         # Install all required dependencies

# Add Callback URL from iNaturalist to redirect_uri in the config.json
# Add Application ID from iNaturalist to app_id in the config.json
# Add the Secret from iNaturalist to app_secret in the config.json

# Generate the access tokens needed by iNaturalist first
python inaturalist_oauth.py -a

# Get the API token from iNaturalist, which will be used in the Authentication header in all the requests
python inaturalist_oauth.py -p

# To print and setup environment variables. You should set these environment variables up in the Heroku app
python inaturalist_oauth.py -o > .env
```

# Usage (after you have set up the authentication from above)
To launch this application, run the following command:
```bash
uvicorn main:app --reload
```

To launch this application to Heroku, first set all the necessary environment variables from the config.json in your Heroku deployment. Then 
run the following command:
```bash
git push heroku main
```

# How to run unit tests
```bash
python -m unittest tests.py
```