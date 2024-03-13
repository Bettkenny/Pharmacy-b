from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token
from models import db,User,Pharmacy,Payment,Drug,Review,Order,Message, bcrypt
from datetime import datetime

class UserRegistrationResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return{"id":user.id,"username":user.username,"gender":user.gender,"email":user.email,"contact":user.contact}
        else:
            return{"message":"User not found"}, 401
        
    def post(self):
        try:
            data = request.get_json()
            username = data.get("username")
            gender = data.get("gender")
            email = data.get("email")
            password = data.get("password")
            contact = data.get("contact")
            date_of_birth = data.get("date_of_birth")
            if not username or not gender or not email or not contact or not date_of_birth:
               return {"error":"All the fields are required !"}
            existing_user = User.query.filter_by(username = username).first()
            if existing_user:
                return{"error":"username is already taken."},400
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            if password is None or not isinstance(password, str):
                return {"error": "password is required"}
            print("Data:", data)
            print("Password:", password)
            new_user = User(username = username,password = hashed_password, email = email, date_of_birth = date_of_birth, contact=contact)
            db.session.add(new_user)
            db.session.commit()
            return {"message":"User registered successfully."}
        except Exception as e:
            return {"error":str (e)}, 500
    def put(self, user_id):
        user = User.query.get(user_id)
        data = request.get_json()
        user.username =data.get('username', user.username)
        user.gender =data.get('gender', user.gender)
        user.email =data.get('email', user.gender)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.contact =data.get('contact', user.contact)
        db.session.commit()
        return{
            "message": "profile updated successfully",
            "user": {
                "id":user.id,
                "username":user.username,
                "gender":user.gender,
                "date_of_birth":user.date_of_birth,
                "email":user.email,
                "contact":user.contact
            }
        }
    def delete(self, user_id):
        user=User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return{"message" "User deleted successfully"}

class UserLoginResource(Resource) :
    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return {"error": "email and password are required"}, 400
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.email)
                refresh_token = create_refresh_token(identity=user.email)
                return{ 
                    "message": "login successfully.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                }, 200
            else:
                return{"error": "invalid email or password"}, 401
        except Exception as e:
            return{"error": str (e)}, 500  

class MessageResource(Resource):
    def get(self):
        messages = Message.query.all()
        if messages:
            return [{"id": message.id, "name":message.name, "email": message.email, "message":message.comment}for message in messages], 200 
        else:
            return{"message": "Non messages found."}, 404
   
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        comment = data.get("comment")
        if not name or not email or not comment:
            return{"error": "All fields (name, email, comment) are required."}, 400
        new_message = Message(name=name, email=email, comment=comment)
        db.session.add(new_message)
        db.session.commit()
        return{"message": "Message added successfully !" , "id": new_message.id}, 201
    
       
class PharmacyResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type = str ,required = True, help = 'Name cannot be blank') 
    parser.add_argument('location' ,type = str, required = True, help = 'location cannot be blank')
    parser.add_argument('image_url' ,type = str, required = True, help = 'image_url cannot be blank')   

    def get(self, pharmacy_id=None):
        if pharmacy_id is None:
            pharmacys = Pharmacy.query.all()
            return [
                {
                    "id": pharmacy.id,
                    "name": pharmacy.name,
                    "location": pharmacy.location,
                    "image_url": pharmacy.image_url,
                }
                for pharmacy in pharmacys
        ]
        pharmacy = Pharmacy.query.get(pharmacy_id)
        if not pharmacy:
            return {"message": "Pharmacy not found."}, 404
        return {
            "id": pharmacy.id,
            "name": pharmacy.name,
            "location": pharmacy.location,
            "image_url": pharmacy.image_url,
        }


    @jwt_required()
    def post(self):
        current_user = User.query.filter_by(email=get_jwt_identity()).first()

        if current_user.role != "admin":
            return {"message": "Access denied! Admins only."}, 403

        data = request.get_json()
        new_pharmacy = Pharmacy(name=data['name'], location=data['location'], image_url=data['image_url'])
        db.session.add(new_pharmacy)
        db.session.commit()
        return {
            "message": "Pharmacy added successfully.",
            "pharmacy": {
                "id": new_pharmacy.id,
                "name": new_pharmacy.name,
                "location": new_pharmacy.location,
                "image_url": new_pharmacy.image_url
            }
        }
    
class AdminPharmacyResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = User.query.filter_by(email = get_jwt_identity()).first()
            if not current_user:
                return {'message': 'Only admins can add pharmacys'}, 401

            data = request.get_json()
            new_pharmacy = Pharmacy(
                name=data['name'],
                location=data['location'],
                image_url=data['image_url']
            )
            db.session.add(new_pharmacy)
            db.session.commit()
            return {
                'message': 'pharmacy added successfully',
                "pharmacy":{
                    "id":new_pharmacy.id,
                    "name": new_pharmacy.name,
                    "location": new_pharmacy.location,
                    "image_url": new_pharmacy.image_url
                }
            }
        except Exception as e:
            return{"error": str (e)}, 500
    

    @jwt_required()
    def patch(self, pharmacy_id):
        try: 
            current_user = User.query.filter_by(email=get_jwt_identity()).first()
            if current_user.role != "admin":
                return {"message": "Access denied! Admins only."}, 403

            pharmacy = Pharmacy.query.get(pharmacy_id)
            if not pharmacy:
                return {"message": "pharmacy not found."}, 404

            data = request.get_json()
            pharmacy.name = data["name"]
            pharmacy.location = data["location"]
            pharmacy.image_url = data.get("image_url") 
            db.session.commit()

            return {
                "message": "pharmacy updated successfully",
                "pharmacy": {
                    "id": pharmacy.id,
                    "name": pharmacy.name,
                    "location": pharmacy.location,
                    "image_url": pharmacy.image_url
                }
            }

        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()
    def delete(self,pharmacy_id):
        current_user = User.query.filter_by(email = get_jwt_identity()).first()
        if current_user.role != "admin":
            return{"message": "Access denied!admins only."},403
        pharmacy = Pharmacy.query.get(pharmacy_id)
        if not pharmacy:
            return{"message":"pharmacy not found."}, 404
        db.session.delete(pharmacy)
        db.session.commit()
        return {"message": "pharmacy deleted successfully.", "pharmacy_id": pharmacy_id}


class DrugResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type = str, required = True, help = 'description cannot be blank')
    parser.add_argument('image_url' ,type = str, required = True, help = 'image_url cannot be blank')  
    parser.add_argument('price' ,type = int, required = True, help = 'price cannot be blank')  
    parser.add_argument('pharmacy_name', type = str, required = True, help = 'pharmacy_name cannot be blank')  
    parser.add_argument('status', type = str, required = True, help = 'status cannot be blank')  
     

    
    def get(self,drug_id = None):
        if drug_id is None:
            drugs = Drug.query.all()
            return [{"id":drug.id,"pharmacy_name":drug.pharmacy_name,"description":drug.description,"image_url":drug.image_url,"status":drug.status,"price":drug.price}for drug in drugs]
        drug = Drug.query.get(drug_id)
        if not drug:
            return{"message":"drug not found."}
        return {
            "id":drug.id,
            "pharmacy_name":drug.pharmacy_name,
            "description":drug.description,
            "image_url":drug.image_url,
            "status":drug.status,
            "price":drug.price
        }
    @jwt_required()
    def post(self):
        current_user = User.query.filter_by(email = get_jwt_identity()).first()
        if current_user.role != "admin":
            return {"message": "Access denied!admins only."},403
        data = request.get_json()
        new_drug = Drug(pharmacy_name =data['pharmacy_name'],description = data['description'],image_url = data['image_url'],status = data['status'],price = data['price'])
        db.session.add(new_drug)
        db.session.commit()
        return {
            "message":"drug added successfully",
            "drug": {
                "id":new_drug.id,
                "pharmacy_name":new_drug.pharmacy_name,
                "description":new_drug.description,
                "image_url":new_drug.image_url,
                "status":new_drug.status,
                "price":new_drug.price
            }
        }

class AdminDrugResource(Resource):
    @jwt_required()
    def post(self):
        current_user = User.query.filter_by(email = get_jwt_identity()).first()
        if current_user .role != "admin":
            return{"Access denied!admins only."},403
        data = request.get_json()
        new_drug =  new_drug = Drug(pharmacy_name =data['pharmacy_name'],description = data['description'],image_url = data['image_url'],status = data['status'],price = data['price'])
        db.session.add(new_drug)
        db.session.commit()
        return {
                "id":new_drug.id,
                "pharmacy_name":new_drug.pharmacy_name,
                "drug_type":new_drug.drug_type,
                "description":new_drug.description,
                "image_url":new_drug.image_url,
                "status":new_drug.status,
                "price":new_drug.price
        }
        
    @jwt_required()
    def put(self, drug_id):
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if current_user.role != "admin":
            return {"message": "Access denied! Admins only."}, 403

        drug = Drug.query.get(drug_id)
        if not drug:
            return {"message": "drug not found."}, 404

        data = request.get_json()
        drug.pharmacy_name = data.get('pharmacy_name', drug.pharmacy_name)
        drug.description = data.get('description', drug.description)
        drug.image_url = data.get('image_url', drug.image_url)
        drug.status = data.get('status', drug.status)
        drug.price = data.get('price', drug.price)

        db.session.commit()

        return {
            "id": drug.id,
            "pharmacy_name": drug.pharmacy_name,
            "description": drug.description,
            "image_url": drug.image_url,
            "status": drug.status,
            "price": drug.price
        }

        
    @jwt_required()
    def delete(self,drug_id):
        current_user = User.query.filter_by(email = get_jwt_identity()).first()
        if current_user.role != "admin":
            return{"Access denied!admins only."},403
        drug = Drug.query.get(drug_id)
        if not drug:
            return{"error":"drug not found."}
        db.session.delete(drug)
        db.session.commit()
        return {"message":"drug deleted successfully."}  
class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        if reviews:
            return[{"id":review.id,"comment":review.comment,"user_id":review.user_id,"drug_id":review.drug_id}for review in reviews]
        else:
            return {"message":"No review added!"},401
        
    def post(self):
        data = request.get_json()
      
        new_review = Review(user_id = data["user_id"],drug_id = data["drug_id"],comment = data["comment"])
        db.session.add(new_review)
        db.session.commit()
        if new_review:
            return {"message":"Review added successfully!"},201
        else:
            return{"error":"Failed to add review!"}

    #@jwt_required()
    def delete(self,review_id):
        """ current_user = User.query.filter_by(email = get_jwt_identity()).first()
        if current_user.role != "admin":
            return{"Access denied.Admin only!"},401 """
        
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return{"Review deleted successfully."},201
        else:
            return{"error":"Review not deleted!"},401
            

class OrdersResources(Resource):
    
    def get(self, user_id=None):
        # Query all orders
        all_orders = Order.query.all()

        if user_id:
            # Query orders associated with the provided user_id
            user_orders = Order.query.filter_by(user_id=user_id).all()
            if not user_orders:
                return {"error": "No orders found for the user."}
            else:
                # Return orders for the specific user
                return {"user_orders": [{"id": order.id, "user_id": order.user_id, "drug_id": order.drug_id,
                                            
                                            "total_price": order.total_price} for order in user_orders],
                        "all_orders": [{"id": order.id, "user_id": order.user_id, "drug_id": order.drug_id,
                                           
                                           "total_price": order.total_price} for order in all_orders]}
        else:
            # Return all orders
            return {"all_orders": [{"id": order.id, "user_id": order.user_id, "drug_id": order.drug_id,
                                      
                                      "total_price": order.total_price} for order in all_orders]}
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        # Convert date strings to datetime objects
       
        newOrder = Order(
            user_id=data['user_id'],
            drug_id=data['drug_id'],
           
            total_price=data['total_price']
        )
        db.session.add(newOrder)
        db.session.commit()

        if newOrder.id:
            return {
                "message": "order made successfully!",
                "user_id": newOrder.user_id,
                "drug_id": newOrder.drug_id,
                
                "total_price": newOrder.total_price
            }, 201
        else:
            return {"error": "Failed. Try again!"}, 400




    def put(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return {"message": "order not found."}, 404

        data = request.get_json()
        order.drug_id = data.get("drug_id", order.drug_id)
        order.user_id = data.get("user_id", order.user_id)
      
        order.total_price = data.get("total_price", order.total_price)

        db.session.commit()

        return {
            "message": "order updated successfully",
            "drug_id": order.drug_id,
            "user_id": order.user_id,
            
            "total_price": order.total_price
        }
class DeleteResources(Resource):
    def delete(self, id):
        order = Order.query.get(id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return {"message": "order deleted successfully."}
        else:
            return {"error": "order not deleted."}

