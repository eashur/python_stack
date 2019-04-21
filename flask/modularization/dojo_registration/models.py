from sqlalchemy.sql import func
from flask import flash
from config import db, bcrypt
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=\S{5,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')



class Users(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(145))
    last_name = db.Column(db.String(145))
    email = db.Column(db.String(125))
    password = db.Column(db.String(125))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if len(user_data["first_name"]) < 1:
            is_valid = False
            flash("Please provide a first name")
        if len(user_data["last_name"]) < 1:
            is_valid = False
            flash("Please provide a last name")
        if not EMAIL_REGEX.match(user_data["email"]):
            is_valid = False
            flash("Please provide a valid email")
        if len(user_data["password"]) < 8:
            is_valid = False
            flash("Password should be at least 8 characters")
        if user_data["password"] != user_data["cpassword"]:
            is_valid = False
            flash("Passwords do not match")
        return is_valid

    @classmethod
    def validate_login(cls, user_data):
        is_valid = True
        result = Users.query.filter_by(email = user_data["username"]).first()

        if not EMAIL_REGEX.match(user_data["username"]):
            is_valid = False
            flash("Please provide a valid email")
        if len(user_data["password"]) < 3:
            is_valid = False
            flash("Password should be at least 8 characters")
        if result:
            if not bcrypt.check_password_hash(result.password, user_data['password']):
                is_valid = False
                flash("Passwords incorrect")
        return is_valid

    @classmethod
    def add_new_user(cls, user_data):
        hashed_password = bcrypt.generate_password_hash(user_data["password"])
        user_to_add = cls(first_name=user_data["first_name"], last_name=user_data["last_name"], email=user_data["email"], password=hashed_password)
        db.session.add(user_to_add)
        db.session.commit()
        return user_to_add

