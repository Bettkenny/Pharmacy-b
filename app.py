from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import Payment
from flask_bcrypt import Bcrypt

from resources import (
    UserRegistrationResource, 
    UserLoginResource,
    MessageResource,
    DrugResource, 
    AdminDrugResource, 
    PharmacyResource,
    AdminPharmacyResource,
    ReviewResource,
    OrdersResources,
    DeleteResources
)
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 36000



migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

db.init_app(app)
api = Api(app)

CORS(app)





# Add resources to API
api.add_resource(UserRegistrationResource, '/register', '/register/<int:user_id>')
api.add_resource(UserLoginResource, '/login')
api.add_resource(MessageResource, '/messages')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')
api.add_resource(DrugResource, '/drugs', '/drugs/<int:drug_id>')
api.add_resource(AdminDrugResource, '/drugs/<int:drug_id>')
api.add_resource(PharmacyResource, '/pharmacy', '/admin/pharmacy', '/admin/pharmacys/<pharmacy_id>')
api.add_resource(AdminPharmacyResource, '/admin/pharmacys', '/admin/pharmacys/<pharmacy_id>')
api.add_resource(OrdersResources, '/orders', '/orders/<int:user_id>', '/orders/<int:id>')
api.add_resource(DeleteResources, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(port=5000)
