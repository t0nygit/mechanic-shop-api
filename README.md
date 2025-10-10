# Mechanic Shop API

A RESTful API built with Flask for managing a mechanic shop's customers, mechanics, and service tickets.

## Features

- **Customer Management**: Full CRUD operations for customers
- **Mechanic Management**: Full CRUD operations for mechanics
- **Service Ticket Management**: Create tickets, assign/remove mechanics
- **Application Factory Pattern**: Modular and scalable code structure with blueprints

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- MySQL
- Postman (for API testing)

## Database Structure

- **Customers**: Store customer information
- **Mechanics**: Store mechanic/employee information
- **Service Tickets**: Track service requests with VIN, descriptions, and dates
- **Many-to-Many Relationship**: Service tickets can have multiple mechanics assigned

## API Endpoints

### Customers
- `POST /customers` - Create a new customer
- `GET /customers` - Get all customers
- `GET /customers/<id>` - Get a specific customer
- `PUT /customers/<id>` - Update a customer
- `DELETE /customers/<id>` - Delete a customer

### Mechanics
- `POST /mechanics` - Create a new mechanic
- `GET /mechanics` - Get all mechanics
- `GET /mechanics/<id>` - Get a specific mechanic
- `PUT /mechanics/<id>` - Update a mechanic
- `DELETE /mechanics/<id>` - Delete a mechanic

### Service Tickets
- `POST /service-tickets` - Create a new service ticket
- `GET /service-tickets` - Get all service tickets
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign a mechanic to a ticket
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove a mechanic from a ticket

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python`
5. Create a MySQL database called `mechanic_shop`
6. Update `config.py` with your MySQL password
7. Run the application: `python3 app.py`

## Testing

Import the included Postman collection (`Mechanic_Shop_API.postman_collection.json`) to test all endpoints.

## Project Structure
mechanic_shop_app/
├── application/
│   ├── init.py          # Application factory
│   ├── extensions.py         # Database and Marshmallow initialization
│   ├── models.py             # Database models
│   └── blueprints/
│       ├── customers/        # Customer routes and schemas
│       ├── mechanics/        # Mechanic routes and schemas
│       └── service_tickets/  # Service ticket routes and schemas
├── app.py                    # Application entry point
└── config.py                 # Configuration settings

## Author

**Tony Bevilacqua**

[GitHub Profile](https://github.com/t0nygit)

Built as part of a backend specialization course.