import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_get_observations(self):
        q = {"lng": 0, "lat": 0}
        response = client.get("/observations", params=q)
        print(response.text)
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