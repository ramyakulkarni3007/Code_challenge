import json
import unittest
from app import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_weather_data(self):
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('results', data)
        self.assertIn('metadata', data)

    def test_get_weather_stats(self):
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('results', data)
        self.assertIn('metadata', data)

if __name__ == '__main__':
    unittest.main()
