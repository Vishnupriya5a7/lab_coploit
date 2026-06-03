"""
Unit Tests for Flask Web Application
Author: Mark (with GitHub Copilot assistance)
Purpose: Test API endpoints and token generation functionality
"""

import unittest
import json
from app import app, generate_token, submissions


class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application"""

    def setUp(self):
        """
        Set up test client and clear submissions before each test.
        This ensures tests are isolated and independent.
        """
        # Create test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear submissions list before each test
        submissions.clear()

    def tearDown(self):
        """Clean up after each test"""
        submissions.clear()

    # ===== Token Generation Tests =====

    def test_generate_token_default_length(self):
        """Test token generation with default length"""
        token = generate_token()
        self.assertEqual(len(token), 16)
        self.assertIsInstance(token, str)

    def test_generate_token_custom_length(self):
        """Test token generation with custom length"""
        token = generate_token(length=32)
        self.assertEqual(len(token), 32)

    def test_generate_token_uniqueness(self):
        """Test that generated tokens are unique"""
        token1 = generate_token()
        token2 = generate_token()
        self.assertNotEqual(token1, token2)

    def test_generate_token_contains_valid_characters(self):
        """Test that token contains only valid alphanumeric characters"""
        token = generate_token()
        self.assertTrue(token.isalnum())

    # ===== Home Page Tests =====

    def test_home_page_get(self):
        """Test GET request to home page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submission Form', response.data)

    def test_home_page_contains_form(self):
        """Test that home page contains form elements"""
        response = self.app.get('/')
        self.assertIn(b'submissionForm', response.data)
        self.assertIn(b'name', response.data)
        self.assertIn(b'reason', response.data)

    # ===== API Endpoint Tests =====

    def test_submit_form_valid_data(self):
        """Test form submission with valid data"""
        payload = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'reason': 'bug_report',
            'comments': 'Found a bug'
        }
        response = self.app.post(
            '/api/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('token', data)
        self.assertEqual(data['data']['name'], 'John Doe')

    def test_submit_form_missing_name(self):
        """Test form submission without name field"""
        payload = {
            'email': 'john@example.com',
            'reason': 'bug_report',
            'comments': 'Found a bug'
        }
        response = self.app.post(
            '/api/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_submit_form_missing_reason(self):
        """Test form submission without reason field"""
        payload = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'comments': 'Found a bug'
        }
        response = self.app.post(
            '/api/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_submit_form_empty_body(self):
        """Test form submission with empty body"""
        response = self.app.post(
            '/api/submit',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_submit_form_generates_token(self):
        """Test that submission generates a unique token"""
        payload = {
            'name': 'Jane Doe',
            'reason': 'feature_request'
        }
        response = self.app.post(
            '/api/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['token'])
        self.assertEqual(len(data['token']), 16)

    def test_submit_form_stores_data(self):
        """Test that submission data is stored"""
        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'reason': 'improvement',
            'comments': 'Test comment'
        }
        response = self.app.post(
            '/api/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0]['name'], 'Test User')

    # ===== Get Submissions Tests =====

    def test_get_submissions_empty(self):
        """Test retrieving submissions when none exist"""
        response = self.app.get('/api/submissions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['submissions']), 0)

    def test_get_submissions_multiple(self):
        """Test retrieving multiple submissions"""
        # Submit multiple forms
        for i in range(3):
            payload = {
                'name': f'User {i}',
                'reason': 'bug_report'
            }
            self.app.post(
                '/api/submit',
                data=json.dumps(payload),
                content_type='application/json'
            )
        
        response = self.app.get('/api/submissions')
        data = json.loads(response.data)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['submissions']), 3)

    # ===== Token Generation Endpoint Tests =====

    def test_get_token_default(self):
        """Test token generation endpoint with default length"""
        response = self.app.get('/api/token')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['token']), 16)

    def test_get_token_custom_length(self):
        """Test token generation endpoint with custom length"""
        response = self.app.get('/api/token?length=32')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['token']), 32)
        self.assertEqual(data['length'], 32)

    def test_get_token_invalid_length_too_short(self):
        """Test token generation with length too short"""
        response = self.app.get('/api/token?length=2')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_get_token_invalid_length_too_long(self):
        """Test token generation with length too long"""
        response = self.app.get('/api/token?length=200')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_get_token_valid_length_boundaries(self):
        """Test token generation at valid boundary values"""
        # Test minimum valid length
        response = self.app.get('/api/token?length=4')
        self.assertEqual(response.status_code, 200)
        
        # Test maximum valid length
        response = self.app.get('/api/token?length=128')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['token']), 128)

    # ===== Health Check Tests =====

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)

    # ===== Error Handling Tests =====

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_invalid_method(self):
        """Test invalid HTTP method"""
        response = self.app.put('/')
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    # Run all tests with verbose output
    unittest.main(verbosity=2)