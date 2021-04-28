import re
import io
import os
import sys

from unittest import TestCase
from unittest import mock
from unittest import main as unittest_main

from fastapi.testclient import TestClient
from main import app

from config_helper import initialize_config
from config_helper import print_config_as_env
from parse_query import parse_query


# No unit tests for inaturalist_oath since it is a script, not a module

client = TestClient(app)

sample_env = {  
                "site": "https://www.inaturalist.org",
                "api_token": "12345",
                "api_token_endpoint": "https://www.inaturalist.org/users/api_token",
                "access_token": "12345",
                "app_id": "12345",
                "app_secret": "12345",
                "redirect_uri": "https://github.com/",
                "created_at": "1",
                "request_endpoint": "https://api.inaturalist.org/v1"
            }

sample_file = {
    "total_results": 0,
    "page": 0,
    "per_page": 0,
    "results": [
        {
            "id": 1234,
            "species_guess": "rattlesnake",
            "geojson": {
                "coordinates": [
                    1.0,   # Longitude
                    1.0     # Latitude
                ],
                "type": "Point",
            },
            "taxon": {
                "wikipedia_url": "www.abc.com",
                "default_photo": {
                    "url": "www.url.com"
                }
            },
            "site_id": 90
        }
    ]
}

sample_output = {
    "results": [
        {
            "id": 1234,
            "species_guess": "rattlesnake",
            "longitude": 1.0,
            "latitude": 1.0,
            "wiki": "www.abc.com",
            "photo": "www.url.com"
        }
    ]
}


class TestAPI(TestCase):
    def test_get_observations(self):
        q = {"lng": 0, "lat": 0}
        response = client.get("/observations", params=q)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_invalid_longitude(self):
        q = {"lng": 182.0, "lat": 70.0}
        response = client.get("/observations", params=q)
        self.assertEqual(response.json(), { "err": "Invalid coordinates."})

        q = {"lng": -190.0, "lat": 70.0}
        response = client.get("/observations", params=q)
        self.assertEqual(response.json(), { "err": "Invalid coordinates."})

    def test_invalid_latitude(self):
        q = {"lng": 70.0, "lat": 91.0}
        response = client.get("/observations", params=q)
        self.assertEqual(response.json(), { "err": "Invalid coordinates."})

        q = {"lng": 70.0, "lat": -100.0}
        response = client.get("/observations", params=q)
        self.assertEqual(response.json(), { "err": "Invalid coordinates."})

class TestParse(TestCase):
    def test_parser(self):
        response = parse_query(sample_file)
        self.assertEqual(response, sample_output)
    
class TestConfigHelper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env_patcher = mock.patch.dict(os.environ, sample_env)
        cls.env_patcher.start()

    def test_initialize_config(self):
        # Assumes you have authentication information inside your environment
        config = {}
        initialize_config(config)
        config["created_at"] = str(config["created_at"])
        self.assertEqual(config, sample_env)

    def test_print_config_as_env(self):
        expected_output = re.compile(r"\w* = .*", flags=re.DOTALL + re.M)
        output = io.StringIO()
        sys.stdout = output
        sample_env["created_at"] = 1
        print_config_as_env(sample_env)
        sys.stdout = sys.__stdout__
        self.assertRegex(output.getvalue(), expected_output)

if __name__ == "__main__":
    unittest_main()
