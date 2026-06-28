# tests.py

from django.test import TestCase, Client
from django.urls import reverse

class SumCalculationTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Get the URL name for the view
        cls.url = reverse('caluclator') 
        # Note: Replace 'your_url_name' with your actual URL pattern name

    def setUp(self):
        # Initialize a client for making requests
        self.client = Client()
        # The template is required for the test to run successfully
        # We simulate the initial page load to get the base response
        self.client.get(self.url)


    # --- TEST CASES ---

    def test_get_request_displays_form(self):
        """Tests that a GET request displays the initial form."""
        response = self.client.get(self.url)
        # Check if the status code is OK
        self.assertEqual(response.status_code, 200)
        # Check if the response contains the name of the expected template
        self.assertContains(response, "Sum Calculator")


    def test_successful_summation(self):
        """Tests the calculation when two valid numbers are provided."""
        # Simulate submitting the form via POST
        payload = {
            'input1': '100',
            'input2': '50.5'
        }
        
        # Send the POST request
        response = self.client.post(self.url, payload)

        # Check for success status code
        self.assertEqual(response.status_code, 200)
        
        # Check if the template context correctly received the result
        self.assertContains(response, "The sum is: 150.5") # Assuming your template displays it like this

    def test_summation_with_zero_and_negative(self):
        """Tests calculation with edge cases like zero and negative numbers."""
        payload = {
            'input1': '-10',
            'input2': '0'
        }
        response = self.client.post(self.url, payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The sum is: -10")


    def test_error_handling_for_non_numeric_first_input(self):
        """Tests that a non-numeric first input returns an error status."""
        payload = {
            'input1': 'abc', # Invalid input
            'input2': '50'
        }
        response = self.client.post(self.url, payload)

        # Expect a 400 Bad Request status code
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Error: First input must be a valid number.")

    def test_error_handling_for_non_numeric_second_input(self):
        """Tests that a non-numeric second input returns an error status."""
        payload = {
            'input1': '10',
            'input2': 'xyz' # Invalid input
        }
        response = self.client.post(self.url, payload)

        # Expect a 400 Bad Request status code
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Error: Second input must be a valid number.")
        
    def test_handling_empty_fields(self):
        """Tests that submitting empty fields triggers a validation error."""
        payload = {
            'input1': '',
            'input2': ''
        }
        # The validation logic must decide how to handle empty strings.
        # Based on the fixed code, empty strings passed to float() raise a ValueError.
        response = self.client.post(self.url, payload)
        
        # We expect one of the validation errors to be returned
        self.assertTrue(
            response.content.decode().startswith("Error: First input must be a valid number.") or 
            response.content.decode().startswith("Error: Second input must be a valid number.")
        )
