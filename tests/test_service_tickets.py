import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app
from application.extensions import db
from application.models import ServiceTicket, Customer, Mechanic, Inventory
from config import TestConfig

class TestServiceTickets(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create a test customer (needed for service tickets)
            self.test_customer = Customer(
                name='Test Customer',
                email='customer@test.com',
                phone='555-1234',
                password='testpass'
            )
            db.session.add(self.test_customer)
            
            # Create a test mechanic
            self.test_mechanic = Mechanic(
                name='Test Mechanic',
                email='mechanic@test.com',
                phone='555-5555',
                salary=50000.00
            )
            db.session.add(self.test_mechanic)
            
            # Create test inventory item
            self.test_part = Inventory(
                name='Test Part',
                price=99.99
            )
            db.session.add(self.test_part)
            
            # Create a test service ticket
            self.test_ticket = ServiceTicket(
                VIN='12345678901234567',
                service_date='2024-01-01',
                service_desc='Test service',
                customer_id=1
            )
            db.session.add(self.test_ticket)
            
            db.session.commit()
            
            self.customer_id = self.test_customer.id
            self.mechanic_id = self.test_mechanic.id
            self.ticket_id = self.test_ticket.id
            self.part_id = self.test_part.id
    
    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_all_service_tickets(self):
        """Test GET /service-tickets/ endpoint"""
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_service_ticket(self):
        """Test POST /service-tickets/ endpoint"""
        new_ticket = {
            'VIN': '98765432109876543',
            'service_date': '2024-02-01',
            'service_desc': 'Oil change',
            'customer_id': self.customer_id
        }
        
        response = self.client.post('/service-tickets/', json=new_ticket)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['VIN'], '98765432109876543')
    
    def test_assign_mechanic_to_ticket(self):
        """Test PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>"""
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        
        self.assertEqual(response.status_code, 200)
    
    def test_remove_mechanic_from_ticket(self):
        """Test PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>"""
        # First assign the mechanic
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        
        # Then remove them
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}')
        
        self.assertEqual(response.status_code, 200)
    
    def test_add_part_to_ticket(self):
        """Test POST /service-tickets/<ticket_id>/add-part/<part_id>"""
        response = self.client.post(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        
        self.assertEqual(response.status_code, 200)
    
    def test_edit_ticket_mechanics(self):
        """Test PUT /service-tickets/<ticket_id>/edit"""
        edit_payload = {
            'add_ids': [self.mechanic_id],
            'remove_ids': []
        }
        
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit', json=edit_payload)
        
        self.assertEqual(response.status_code, 200)
    
    def test_create_ticket_invalid_customer(self):
        """Test POST /service-tickets/ with invalid customer (NEGATIVE TEST)"""
        invalid_ticket = {
            'VIN': '11111111111111111',
            'service_date': '2024-03-01',
            'service_desc': 'Test',
            'customer_id': 999  # Non-existent customer
        }
        
        response = self.client.post('/service-tickets/', json=invalid_ticket)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()