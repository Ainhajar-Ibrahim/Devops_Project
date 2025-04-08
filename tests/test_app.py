import unittest
from unittest.mock import patch
from app import app  # Assuming the Flask app is saved in a file named 'app.py'

class TestApp(unittest.TestCase):

    @patch('requests.get')  # Mocking the 'requests.get' method
    def test_get_version(self, mock_get):
        # Create a test client for the Flask app
        client = app.test_client()
        
        # Make a GET request to the /version endpoint
        response = client.get('/version')
        
        # Check the response status code
        self.assertEqual(response.status_code, 200)
        
        # Check the response data
        self.assertIn('Current app version: 1.0.0', response.data.decode('utf-8'))

    @patch('requests.get')  # Mocking the 'requests.get' method
    def test_get_temperature_success(self, mock_get):
        # Sample data to mock the API response
        mock_response = {
            "sensors": [
                {
                    "title": "Temperatur",
                    "lastMeasurement": {"value": 22.5}
                }
            ]
        }
        
        # Mock the response from the external API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Create a test client for the Flask app
        client = app.test_client()
        
        # Make a GET request to the /temperature endpoint
        response = client.get('/temperature')
        
        # Check the response status code
        self.assertEqual(response.status_code, 200)
        
        # Check the temperature value in the response
        response_json = response.get_json()  # Parse the response to a Python dictionary
        self.assertEqual(response_json['temperature'], 22.5)

    @patch('requests.get')  # Mocking the 'requests.get' method
    def test_get_temperature_sensor_not_found(self, mock_get):
        # Sample data where the sensor is not found
        mock_response = {
            "sensors": [
                {
                    "title": "Humidity",
                    "lastMeasurement": {"value": 50}
                }
            ]
        }
        
        # Mock the response from the external API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Create a test client for the Flask app
        client = app.test_client()
        
        # Make a GET request to the /temperature endpoint
        response = client.get('/temperature')
        
        # Check the response status code
        self.assertEqual(response.status_code, 404)
        
        # Check the error message in the response
        response_json = response.get_json()  # Parse the response to a Python dictionary
        self.assertEqual(response_json['error'], 'Temperature sensor not found')

    @patch('requests.get')  # Mocking the 'requests.get' method
    def test_get_temperature_api_failure(self, mock_get):
        # Mock the response from the external API when it fails
        mock_get.return_value.status_code = 500
        
        # Create a test client for the Flask app
        client = app.test_client()
        
        # Make a GET request to the /temperature endpoint
        response = client.get('/temperature')
        
        # Check the response status code
        self.assertEqual(response.status_code, 500)
        
        # Check the error message in the response
        response_json = response.get_json()  # Parse the response to a Python dictionary
        self.assertEqual(response_json['error'], 'Failed to fetch data from the API')


if __name__ == '__main__':
    unittest.main()
