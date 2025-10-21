# Mechanic Shop API

A comprehensive RESTful API built with Flask for managing a mechanic shop's customers, mechanics, service tickets, and inventory.

## Features

- **Customer Management**: Full CRUD operations with token authentication
- **Mechanic Management**: Full CRUD operations with activity tracking
- **Service Ticket Management**: Create tickets, assign/remove mechanics, add parts
- **Inventory Management**: Track parts and supplies with pricing
- **Token Authentication**: Secure login system with JWT tokens
- **Rate Limiting**: Protection against abuse and DDOS attacks
- **Caching**: Improved performance for frequently accessed data
- **Advanced Queries**: Sorting, filtering, and pagination support

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Flask-Limiter
- Flask-Caching
- PyJWT (Token Authentication)
- MySQL
- Postman (API Testing)

## Database Structure

- **Customers**: Store customer information with authentication
- **Mechanics**: Store mechanic/employee information
- **Service Tickets**: Track service requests with VIN, descriptions, and dates
- **Inventory**: Track parts and supplies with pricing
- **Many-to-Many Relationships**: 
  - Service tickets can have multiple mechanics assigned
  - Service tickets can have multiple parts/inventory items

## API Endpoints

### Customers
- `POST /customers` - Create a new customer (Rate Limited: 5/hour)
- `GET /customers` - Get all customers (Cached, Paginated)
- `GET /customers/<id>` - Get a specific customer
- `PUT /customers/<id>` - Update a customer (Token Required)
- `DELETE /customers/<id>` - Delete a customer (Token Required)
- `POST /customers/login` - Login and receive JWT token
- `GET /customers/my-tickets` - Get authenticated customer's tickets (Token Required)

### Mechanics
- `POST /mechanics` - Create a new mechanic (Rate Limited: 10/hour)
- `GET /mechanics` - Get all mechanics
- `GET /mechanics/<id>` - Get a specific mechanic
- `PUT /mechanics/<id>` - Update a mechanic
- `DELETE /mechanics/<id>` - Delete a mechanic
- `GET /mechanics/most-active` - Get mechanics sorted by ticket count

### Service Tickets
- `POST /service-tickets` - Create a new service ticket
- `GET /service-tickets` - Get all service tickets
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign a mechanic
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove a mechanic
- `PUT /service-tickets/<ticket_id>/edit` - Add/remove multiple mechanics at once
- `POST /service-tickets/<ticket_id>/add-part/<part_id>` - Add inventory part to ticket

### Inventory
- `POST /inventory` - Create a new inventory item
- `GET /inventory` - Get all inventory items
- `GET /inventory/<id>` - Get a specific inventory item
- `PUT /inventory/<id>` - Update an inventory item
- `DELETE /inventory/<id>` - Delete an inventory item

## Setup Instructions

1. Clone the repository
```bash
git clone <your-repo-url>
cd mechanic_shop_app
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python flask-limiter flask-caching pyjwt
```

4. Set up MySQL database
```sql
CREATE DATABASE mechanic_shop;
```

5. Configure your database
- Copy `config_example.py` to `config.py`
- Update `config.py` with your MySQL password

6. Run the application
```bash
python3 app.py
```

The API will be available at `http://127.0.0.1:5000`

## Testing

Import the included Postman collection (`Mechanic_Shop_API_Final.postman_collection.json`) to test all endpoints.

### Authentication
Most protected routes require a Bearer Token:
1. Create a customer or login with existing credentials
2. Use the returned token in the Authorization header
3. Format: `Bearer <your-token-here>`

## Project Structure
```
mechanic_shop_app/
├── application/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Flask extensions (db, ma, limiter, cache)
│   ├── models.py                # Database models
│   ├── utils/
│   │   └── util.py              # Token encoding/decoding and decorators
│   └── blueprints/
│       ├── customers/           # Customer routes, schemas, and authentication
│       ├── mechanics/           # Mechanic routes and schemas
│       ├── service_tickets/     # Service ticket routes and schemas
│       └── inventory/           # Inventory routes and schemas
├── app.py                       # Application entry point
├── config.py                    # Configuration (gitignored)
├── config_example.py            # Configuration template
└── Mechanic_Shop_API_Final.postman_collection.json
```

## Security Features

- **Password Storage**: Customer passwords stored in database
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Prevents abuse on customer and mechanic creation
- **Protected Routes**: Update/delete operations require authentication

## Performance Features

- **Caching**: GET customers endpoint cached for 60 seconds
- **Pagination**: Efficient data retrieval for large datasets
- **Optimized Queries**: SQLAlchemy relationships for efficient joins

## Author

**Tony Bevilacqua**

[GitHub Profile](https://github.com/t0nygit)

Built as the final project for Backend Specialization Module 1 - Advanced API Development.