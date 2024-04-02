from app import app, db
from models import User, Pharmacy, Drug
from flask_bcrypt import Bcrypt
from datetime import datetime

# Initialize bcrypt
bcrypt = Bcrypt()

# Define the user data with hashed password
user_data = {
    "username": "ben03",
    "email": "benn@gmail.com",
    "contact": "0741409419",
    "role": "admin",
    # Hashed password for "ben123"
    "password": bcrypt.generate_password_hash("ben123").decode('utf-8'),
    "date_of_birth": datetime(1990, 1, 1),
    "gender": "male"  
}

# Update the user data
with app.app_context():
    user = User.query.filter_by(email=user_data["email"]).first()
    if not user:
        user = User(**user_data)
        db.session.add(user)

# Define pharmacy data
pharmacy_data = {
    "name": "Nyaribo Pharmacy",
    "location": "Nyeri",
    "image_url": "https://qwetu.co.ke/assets/building-bba71653.jpg",
}

# Update the pharmacy data
with app.app_context():
    pharmacy = Pharmacy.query.filter_by(name=pharmacy_data["name"]).first()
    if not pharmacy:
        pharmacy = Pharmacy(**pharmacy_data)
        db.session.add(pharmacy)

# Define drugs data
drugs_data = [
    {
        "pharmacy_name": "Ozempic",
        "drug_category": "Ozzempics",
        "drug_name": "Ozempicc",
        "quantity": "1000g",
        "price": 1200,
        "status": "available",
        "image_url": "https://static.scientificamerican.com/sciam/cache/file/FB689D8D-8D24-43DA-A6F4473B4B1BD271_source.jpg?w=1200",
        "description": "Aspirin is used for pain relief, fever reduction, and inflammation. It's commonly used for headaches, muscle aches, and arthritis. Caution is advised due to potential side effects and interactions."
    },
    {
        "pharmacy_name": "Pushing bills",
        "drug_category": "Bills",
        "drug_name": "Pushing bills",
        "quantity": "500g",
        "price": 400,
        "status": "available",
        "image_url": "https://smartcdn.gprod.postmedia.digital/nationalpost/wp-content/uploads/2014/02/pills11.jpg?quality=90&strip=all&w=288&h=216&sig=2D93uxxaeYYPTXtosNL4jw",
        "description": "Aspirin is used for pain relief, fever reduction, and inflammation. It's commonly used for headaches, muscle aches, and arthritis. Caution is advised due to potential side effects and interactions."
    },
    {
        "pharmacy_name": "Serotinin",
        "drug_category": "Serotinin bills",
        "drug_name": "Serotinin",
        "quantity": "100g",
        "price": 400,
        "status": "available",
        "image_url": "https://www.verywellmind.com/thmb/65iDQks9qrMcgO53ixhuMQP_7v4=/2112x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-858253-001-57a0e7525f9b589aa9efd48b.jpg",
        "description": "Chloroquine is used for pain relief, fever reduction, and inflammation. It's commonly used for headaches, muscle aches, and arthritis. Caution is advised due to potential side effects and interactions."
    },
    {
        "pharmacy_name": "Maramoja",
        "drug_category": "painkiller",
        "drug_name": "Maramoja",
        "quantity": "500g",
        "price": 400,
        "status": "available",
        "image_url": "https://d2jx2rerrg6sh3.cloudfront.net/image-handler/picture/2021/1/shutterstock_544348294.jpg",
        "description": "Chloroquine is used for pain relief, fever reduction, and inflammation. It's commonly used for headaches, muscle aches, and arthritis. Caution is advised due to potential side effects and interactions."
    }
]


with app.app_context():
    for drug_data in drugs_data:
        drug = Drug(**drug_data)
        db.session.add(drug)

    
    db.session.commit()
    print("Updated successfully")
