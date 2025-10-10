from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.extensions import db
from application.models import ServiceTicket, Mechanic, Customer
from application.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from application.blueprints.service_tickets import service_tickets_bp

# CREATE - POST a new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if customer exists
    customer = db.session.get(Customer, ticket_data.customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    # ticket_data is already a ServiceTicket instance, so just add it
    db.session.add(ticket_data)
    db.session.commit()
    
    return service_ticket_schema.jsonify(ticket_data), 201


# READ - GET all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200


# ASSIGN - PUT assign a mechanic to a service ticket
@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    # Check if mechanic is already assigned
    if mechanic in ticket.mechanics:
        return jsonify({"error": "Mechanic already assigned to this ticket."}), 400
    
    # Add mechanic to the ticket's mechanics list
    ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return jsonify({"message": f"Mechanic {mechanic_id} assigned to ticket {ticket_id}."}), 200


# REMOVE - PUT remove a mechanic from a service ticket
@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    # Check if mechanic is assigned
    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this ticket."}), 400
    
    # Remove mechanic from the ticket's mechanics list
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    
    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}."}), 200