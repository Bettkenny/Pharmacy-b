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
            if not username or not gender or not email or not contact or not date_of_birth
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
        Messages = Message.query.all()
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
    


