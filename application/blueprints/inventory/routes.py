from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.extensions import db
from application.models import Inventory
from application.blueprints.inventory.schemas import inventory_schema, inventories_schema
from application.blueprints.inventory import inventory_bp

# CREATE - POST a new inventory item
@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.add(inventory_data)
    db.session.commit()
    
    return inventory_schema.jsonify(inventory_data), 201


# READ - GET all inventory items
@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    query = select(Inventory)
    inventory = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventory), 200


# READ - GET a specific inventory item by ID
@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    
    return inventory_schema.jsonify(item), 200


# UPDATE - PUT update an inventory item
@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    
    try:
        update_data = request.json
        
        if 'name' in update_data:
            item.name = update_data['name']
        if 'price' in update_data:
            item.price = update_data['price']
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    db.session.commit()
    return inventory_schema.jsonify(item), 200


# DELETE - DELETE an inventory item
@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({"message": f"Inventory item id: {inventory_id} successfully deleted."}), 200