import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app
from application.extensions import db
from config import TestConfig

class TestCustomers(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app()
        self.app.config.from_object(TestConfig)  # Use test config
        self.client = self.app.test_client()
        
        # Create all tables in test database
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_all_customers(self):
        """Test GET /customers endpoint"""
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
    
    def test_customer_login_success(self):
        """Test successful customer login"""
        # Create a test user
        new_customer = {
            'name': 'Test User',
            'email': 'testuser@email.com',
            'phone': '555-1234',
            'password': 'testpass'
        }
        
        create_response = self.client.post('/customers/', json=new_customer)
        print(f"Created customer: {create_response.status_code}")
        print(f"Create error: {create_response.get_json()}")  # <-- ADD THIS LINE
        
        # Login with that user
        login_payload = {
            'email': 'testuser@email.com',
            'password': 'testpass'
        }
        
        response = self.client.post('/customers/login', json=login_payload)
        data = response.get_json()
        
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {data}")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', data)
        self.assertIsNotNone(data['auth_token'])

if __name__ == '__main__':
    unittest.main()