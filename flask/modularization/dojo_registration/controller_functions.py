from flask import Flask, render_template, redirect, request, session, flash
from config import app, db
from models import Users

def index():
    
    # list_of_all_dojos = Users.query.all()

    return render_template("index.html" )

def add_newuser():
    validation_check = Users.validate_user(request.form)
    if not validation_check:        
       return redirect("/")
    else:
        flash("Successfully registered, Please login!!!")
        new_user = Users.add_new_user(request.form)
        session["user_id"] = new_user.id
        return redirect("/")

def login():
    validation_check = Users.validate_login(request.form)
    if not validation_check:        
       return redirect("/")
    else:
        list_of_all_users = Users.query.all()
        result = Users.query.filter_by(email = request.form["username"]).first()
        return render_template("users.html", users = list_of_all_users, name = result.first_name )

def logout():
    session.clear()

    return redirect("/")

def follow():
    flash("This function is still in development!!!!")

    return redirect("/login")