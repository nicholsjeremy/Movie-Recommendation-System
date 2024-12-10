import unittest
from src.flask_app.app import app

class RecommendationTest(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.client = app.test_client()
        self.client.testing = True

    def test_recommend_endpoint(self):
        # Test endpoint with a sample user ID (e.g., 1)
        response = self.client.get('/recommend/1')
        
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check if response contains a list of recommendations as a comma-separated string
        data = response.get_data(as_text=True)
        self.assertTrue(isinstance(data, str) and len(data) > 0)

if __name__ == '__main__':
    unittest.main()
