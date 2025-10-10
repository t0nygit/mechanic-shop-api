from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.extensions import db
from application.models import Mechanic
from application.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from application.blueprints.mechanics import mechanics_bp

# CREATE - POST a new mechanic
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if email already exists
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().first()
    
    if existing_mechanic:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    
    return mechanic_schema.jsonify(new_mechanic), 201


# READ - GET all mechanics
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics), 200


# READ - GET a specific mechanic by ID
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    return mechanic_schema.jsonify(mechanic), 200


# UPDATE - PUT update a mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# DELETE - DELETE a mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    
    return jsonify({"message": f"Mechanic id: {mechanic_id} successfully deleted."}), 200