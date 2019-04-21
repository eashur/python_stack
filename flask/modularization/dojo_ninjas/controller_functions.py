from flask import Flask, render_template, redirect, request
from config import app, db
from models import Dojo, Ninja

def index():
    mydict={}
    list_of_all_dojos = Dojo.query.all()

    for i in range (0, len(list_of_all_dojos)):
        print(i)
        each_dojo=Dojo.query.get(i+1)
        students = each_dojo.dojo_ninjas
        mydict[each_dojo]=students
    print(mydict)
    return render_template("dojo.html", dojos= list_of_all_dojos, students = mydict )

def newdojo():
   
    new_instance_of_a_dojo = Dojo(name=request.form['name'], \
        city=request.form['city'], State=request.form['state'])
    db.session.add(new_instance_of_a_dojo)
    db.session.commit()

    return redirect("/")

def newuser():
    print(request.form)
    dojo_n=request.form['dojo_name']
    print(dojo_n)
    list_of_all_dojos = Dojo.query.all()
   
    which_dojo=Dojo.query.filter_by(name=dojo_n).first()
    print(which_dojo.id)
    print(request.form)
    # # dojo_num=which_dojo["id"]

    new_instance_of_a_ninja = Ninja(first_name=request.form['first_name'], \
    last_name=request.form['last_name'], dojo_id=which_dojo.id)
    print(new_instance_of_a_ninja)
    db.session.add(new_instance_of_a_ninja)
    db.session.commit()

    return redirect("/")