from app  import app, db
from models import Pharmacy,  Drug, User

user_data = {
    "username": "ken",
    "email": "mweno@gmail.com",
    "contact": "0741409419",
    "role": "admin",
    "password": "ken123"
}
with app.app_context():
    user = User.query.filter_by(email=user_data["email"]).first()
    if not user:
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

pharmacy_data = {
     "name": "Dawa Pharmacy",
     "location": "Nyeri",
     "image_url": "https://qwetu.co.ke/assets/building-bba71653.jpg"

}
with app.app_context():
    pharmacy = Pharmacy.query.filter_by(name=pharmacy_data["name"]).first()
    if not pharmacy:
        pharmacy = Pharmacy(**pharmacy_data)
        db.session.add(pharmacy)
        db.session.commit()

drugs_data =[
    {
      "pharmacy_name": "Dawa Pharmacy",
      "drug_category": "antibiotics",
      "drug_name": "penadols",
      "quantity": "1000g",
      "price": 1200,
      "status": "available",
      "image_url": "https://i-cf65.ch-static.com/content/dam/cf-consumer-healthcare/panadol/en_pk/pakistan_product/panadol-extra/408x300-panadol-extra.png?auto=format",
      "description": "Penadol Extra is a pain relief medication containing paracetamol and caffeine. It's commonly used to alleviate headaches, muscle aches, and other minor pains. Users should follow dosage instructions and consult a healthcare provider if needed."
    },
    {
      "pharmacy_name": "Dawa Pharmacy",
      "drug_category": "analgesics",
      "drug_name": "aspirin",
      "quantity": "500g",
      "price": 400,
      "status": "available",
      "image_url": "https://m.media-amazon.com/images/I/71sFt1-svKL.jpg",
      "description": "Aspirin is used for pain relief, fever reduction, and inflammation. It's commonly used for headaches, muscle aches, and arthritis. Caution is advised due to potential side effects and interactions."
    }
]
with app.app_context():
    for drug_data in drugs_data:
        drug = Drug(**drug_data)
        db.session.add (drug)
        db.session.commit()
        print ("updated successfully")



