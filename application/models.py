from application.extensions import db

# Customer Model
class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    # Relationship: one customer can have many service tickets
    service_tickets = db.relationship('ServiceTicket', backref='customer', lazy=True)


# ServiceTicket Model
class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.String(20), nullable=False)
    service_desc = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    # Many-to-many relationship with mechanics through junction table
    mechanics = db.relationship('Mechanic', secondary='service_mechanics', backref='service_tickets')


# Mechanic Model
class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Float, nullable=False)


# Junction Table for Many-to-Many relationship
service_mechanics = db.Table('service_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)