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

# UPDATE - PUT edit mechanics on a service ticket
@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    """
    Edit mechanics assigned to a service ticket
    Pass in arrays of mechanic IDs to add or remove
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    data = request.json
    remove_ids = data.get('remove_ids', [])  # List of mechanic IDs to remove
    add_ids = data.get('add_ids', [])        # List of mechanic IDs to add
    
    # Remove mechanics
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
    
    # Add mechanics
    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
    
    db.session.commit()
    
    return jsonify({
        "message": f"Ticket {ticket_id} mechanics updated successfully",
        "mechanics": [{"id": m.id, "name": m.name} for m in ticket.mechanics]
    }), 200

# ADD PART - POST add a part to a service ticket
@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['POST'])
def add_part_to_ticket(ticket_id, part_id):
    """
    Add an inventory part to a service ticket
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    from application.models import Inventory
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Inventory item not found."}), 404
    
    # Check if part is already on the ticket
    if part in ticket.parts:
        return jsonify({"error": "Part already added to this ticket."}), 400
    
    # Add part to the ticket
    ticket.parts.append(part)
    db.session.commit()
    
    return jsonify({
        "message": f"Part '{part.name}' added to ticket {ticket_id}",
        "parts": [{"id": p.id, "name": p.name, "price": p.price} for p in ticket.parts]
    }), 200