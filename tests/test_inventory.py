import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app
from application.extensions import db
from application.models import Inventory
from config import TestConfig

class TestInventory(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create a test inventory item
            self.test_item = Inventory(
                name='Test Part',
                price=99.99
            )
            db.session.add(self.test_item)
            db.session.commit()
            self.item_id = self.test_item.id
    
    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_all_inventory(self):
        """Test GET /inventory/ endpoint"""
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_inventory_item(self):
        """Test POST /inventory/ endpoint"""
        new_item = {
            'name': 'New Part',
            'price': 149.99
        }
        
        response = self.client.post('/inventory/', json=new_item)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'New Part')
        self.assertEqual(data['price'], 149.99)
    
    def test_get_inventory_item_by_id(self):
        """Test GET /inventory/<id> endpoint"""
        response = self.client.get(f'/inventory/{self.item_id}')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Test Part')
    
    def test_update_inventory_item(self):
        """Test PUT /inventory/<id> endpoint"""
        update_payload = {
            'name': 'Updated Part',
            'price': 199.99
        }
        
        response = self.client.put(f'/inventory/{self.item_id}', json=update_payload)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Updated Part')
        self.assertEqual(data['price'], 199.99)
    
    def test_delete_inventory_item(self):
        """Test DELETE /inventory/<id> endpoint"""
        response = self.client.delete(f'/inventory/{self.item_id}')
        
        self.assertEqual(response.status_code, 200)
    
    def test_get_nonexistent_item(self):
        """Test GET /inventory/<id> with invalid ID (NEGATIVE TEST)"""
        response = self.client.get('/inventory/999')
        
        self.assertEqual(response.status_code, 404)
    
    def test_create_inventory_missing_field(self):
        """Test POST /inventory/ with missing field (NEGATIVE TEST)"""
        invalid_item = {
            'name': 'Invalid Item'
            # Missing price
        }
        
        response = self.client.post('/inventory/', json=invalid_item)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()