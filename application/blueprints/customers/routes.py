from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.extensions import db, limiter, cache
from application.models import Customer
from application.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from application.blueprints.customers import customers_bp
from application.utils.util import encode_token, token_required

# CREATE - POST a new customer
@customers_bp.route('/', methods=['POST'])
@limiter.limit("5 per hour")  # Limit: Only 5 customer creations per hour per IP
def create_customer():
    # Rate limiting prevents spam account creation and protects against DDOS attacks
    # where malicious actors could overwhelm our database with fake customer accounts
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if email already exists (customer_data is now a Customer object)
    query = select(Customer).where(Customer.email == customer_data.email)
    existing_customer = db.session.execute(query).scalars().first()
    
    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    # customer_data is already a Customer object, so just add it
    db.session.add(customer_data)
    db.session.commit()
    
    return customer_schema.jsonify(customer_data), 201


# READ - GET all customers (with pagination)
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)  # Cache for 60 seconds
def get_customers():
    # Caching reduces repetitive database queries for frequently accessed data
    # Since customer lists don't change constantly, caching improves response time
    # and reduces database load
    
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)  # Default to page 1
    page_size = request.args.get('page_size', 10, type=int)  # Default to 10 per page
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Query with pagination
    query = select(Customer).limit(page_size).offset(offset)
    customers = db.session.execute(query).scalars().all()
    
    # Get total count for metadata
    total_query = select(db.func.count(Customer.id))
    total_customers = db.session.execute(total_query).scalar()
    
    # Return paginated response with metadata
    return jsonify({
        "customers": customers_schema.dump(customers),
        "page": page,
        "page_size": page_size,
        "total_customers": total_customers,
        "total_pages": (total_customers + page_size - 1) // page_size
    }), 200


# READ - GET a specific customer by ID
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    return customer_schema.jsonify(customer), 200


# UPDATE - PUT update a customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(auth_customer_id, customer_id):
    """
    Protected route - customers must be logged in to update their account
    """
    # Verify the authenticated customer is updating their own account
    if auth_customer_id != customer_id:
        return jsonify({"error": "You can only update your own account"}), 403
    
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        # Get the raw JSON data
        update_data = request.json
        
        # Update each field manually
        if 'name' in update_data:
            customer.name = update_data['name']
        if 'email' in update_data:
            customer.email = update_data['email']
        if 'phone' in update_data:
            customer.phone = update_data['phone']
        if 'password' in update_data:
            customer.password = update_data['password']
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200


# DELETE - DELETE a customer
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(auth_customer_id, customer_id):
    """
    Protected route - customers must be logged in to delete their account
    """
    # Verify the authenticated customer is deleting their own account
    if auth_customer_id != customer_id:
        return jsonify({"error": "You can only delete your own account"}), 403
    
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({"message": f"Customer id: {customer_id} successfully deleted."}), 200


# LOGIN - POST login and get token
@customers_bp.route('/login', methods=['POST'])
def login():
    """
    Login route that validates customer credentials and returns a JWT token
    """
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    email = credentials['email']
    password = credentials['password']
    
    # Query for customer with this email
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()
    
    # Validate credentials (simple password check for now)
    if customer and customer.password == password:
        # Generate token
        auth_token = encode_token(customer.id)
        
        response = {
            "status": "success",
            "message": "Successfully logged in",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': "Invalid email or password"}), 401
    
    
    # GET MY TICKETS - requires token authentication
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    """
    Protected route that returns service tickets for the authenticated customer
    The customer_id is extracted from the JWT token by the @token_required decorator
    """
    # Query service tickets for this customer
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    # Import service ticket schema
    from application.blueprints.service_tickets.schemas import service_tickets_schema
    
    # Return customer's service tickets
    return service_tickets_schema.jsonify(customer.service_tickets), 200