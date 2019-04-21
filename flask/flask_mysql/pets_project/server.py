from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app=Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('my_pets')
    pets_query = mysql.query_db('Select * from my_pets.pets;')

    print(pets_query)

    return render_template("index.html", pets = pets_query)

@app.route("/add_pet", methods = ["POST"])
def add_pets():
    print (request.form)
    mysql = connectToMySQL('my_pets')
    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(pname)s, %(ptype)s, now(), now());"
    
    data ={
        'pname': request.form['name'],
        'ptype': request.form['type']
    }
    # new_pet = mysql.query_db(query)
    new_pet = mysql.query_db(query, data)
    return redirect("/")


if __name__== "__main__":
    app.run(debug=True)