import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app
from application.extensions import db
from application.models import Customer
from config import TestConfig

class TestCustomers(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create a test customer
            self.test_customer = Customer(
                name='Test User',
                email='test@email.com',
                phone='555-1234',
                password='testpass'
            )
            db.session.add(self.test_customer)
            db.session.commit()
            self.customer_id = self.test_customer.id
    
    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_all_customers(self):
        """Test GET /customers/ endpoint"""
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_customer(self):
        """Test POST /customers/ endpoint"""
        new_customer = {
            'name': 'John Doe',
            'email': 'john@email.com',
            'phone': '555-9999',
            'password': 'password123'
        }
        
        response = self.client.post('/customers/', json=new_customer)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'John Doe')
    
    def test_customer_login_success(self):
        """Test successful customer login"""
        credentials = {
            'email': 'test@email.com',
            'password': 'testpass'
        }
        
        response = self.client.post('/customers/login', json=credentials)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', data)
        
        return data['auth_token']
    
    def test_customer_login_invalid(self):
        """Test login with invalid credentials (NEGATIVE TEST)"""
        credentials = {
            'email': 'wrong@email.com',
            'password': 'wrongpass'
        }
        
        response = self.client.post('/customers/login', json=credentials)
        
        self.assertEqual(response.status_code, 401)
    
    def test_update_customer_with_token(self):
        """Test PUT /customers/<id> with authentication"""
        # Get token
        token = self.test_customer_login_success()
        
        # Update payload
        update_payload = {
            'name': 'Updated Name',
            'phone': '555-0000'
        }
        
        # Add token to headers
        headers = {'Authorization': f'Bearer {token}'}
        
        # Use the customer_id in the URL
        response = self.client.put(f'/customers/{self.customer_id}', 
                                   json=update_payload, 
                                   headers=headers)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Updated Name')
    
    def test_update_customer_without_token(self):
        """Test PUT /customers/<id> WITHOUT token (NEGATIVE TEST)"""
        update_payload = {
            'name': 'Updated Name'
        }
        
        # No token!
        response = self.client.put(f'/customers/{self.customer_id}', 
                                   json=update_payload)
        
        self.assertEqual(response.status_code, 401)
    
    def test_delete_customer_with_token(self):
        """Test DELETE /customers/<id> with authentication"""
        token = self.test_customer_login_success()
        headers = {'Authorization': f'Bearer {token}'}
        
        response = self.client.delete(f'/customers/{self.customer_id}', 
                                      headers=headers)
        
        self.assertEqual(response.status_code, 200)
    
    def test_get_my_tickets(self):
        """Test GET /customers/my-tickets (token protected)"""
        token = self.test_customer_login_success()
        headers = {'Authorization': f'Bearer {token}'}
        
        response = self.client.get('/customers/my-tickets', headers=headers)
        
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()