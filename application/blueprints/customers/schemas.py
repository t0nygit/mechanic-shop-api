from application.extensions import ma
from application.models import Customer
from marshmallow import fields

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True
        load_instance = True

# For login - only email and password
class LoginSchema(ma.Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()