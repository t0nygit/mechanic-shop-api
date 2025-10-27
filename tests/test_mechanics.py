import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app
from application.extensions import db
from application.models import Mechanic
from config import TestConfig

class TestMechanics(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create a test mechanic
            self.test_mechanic = Mechanic(
                name='Test Mechanic',
                email='mechanic@test.com',
                phone='555-1111',
                salary=50000.00
            )
            db.session.add(self.test_mechanic)
            db.session.commit()
            self.mechanic_id = self.test_mechanic.id
    
    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_all_mechanics(self):
        """Test GET /mechanics/ endpoint"""
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_mechanic(self):
        """Test POST /mechanics/ endpoint"""
        new_mechanic = {
            'name': 'New Mechanic',
            'email': 'new@mechanic.com',
            'phone': '555-2222',
            'salary': 60000.00
        }
        
        response = self.client.post('/mechanics/', json=new_mechanic)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'New Mechanic')
    
    def test_get_mechanic_by_id(self):
        """Test GET /mechanics/<id> endpoint"""
        response = self.client.get(f'/mechanics/{self.mechanic_id}')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Test Mechanic')
    
    def test_update_mechanic(self):
        """Test PUT /mechanics/<id> endpoint"""
        update_payload = {
            'name': 'Updated Mechanic',
            'email': 'updated@mechanic.com',
            'phone': '555-3333',
            'salary': 70000.00
        }
        
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=update_payload)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Updated Mechanic')
    
    def test_delete_mechanic(self):
        """Test DELETE /mechanics/<id> endpoint"""
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        
        self.assertEqual(response.status_code, 200)
    
    def test_get_most_active_mechanics(self):
        """Test GET /mechanics/most-active endpoint"""
        response = self.client.get('/mechanics/most-active')
        
        self.assertEqual(response.status_code, 200)
    
    def test_create_mechanic_missing_field(self):
        """Test POST /mechanics/ with missing field (NEGATIVE TEST)"""
        invalid_mechanic = {
            'name': 'Invalid Mechanic',
            # Missing email, phone, salary
        }
        
        response = self.client.post('/mechanics/', json=invalid_mechanic)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()