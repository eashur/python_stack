from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app=Flask(__name__)
@app.route("/users")
def index():
    mysql = connectToMySQL('new_friends')
    users_query = mysql.query_db('Select * from new_friends.friends;')

    print(users_query)

    return render_template("users.html", users = users_query)


@app.route("/users/new")
def add_user_page():
    return render_template("add_user.html")


@app.route("/users/<user_id>")
def show_user_page(user_id):
    print (user_id)
    mysql = connectToMySQL('new_friends')
    query = "Select * from new_friends.friends where id = {};".format(int(user_id))
    
    print (query)
    user_query = mysql.query_db(query)
    print (user_query)
    print (user_query[0].get("id"))

    return render_template("show.html", user = user_query)



@app.route("/users/add_user", methods = ["POST"])
def add_users():
    print("$"*50)
    print (request.form)
    mysql = connectToMySQL('new_friends')
    query = "INSERT INTO new_friends.friends (first_name, last_name, email) VALUES (%(fname)s, %(lname)s, %(uemail)s);"
    
    data ={
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'uemail': request.form['email']
    }
    print(query)
    user_id = mysql.query_db(query, data)

    return redirect("/users/{}".format(int(user_id)))
   
@app.route("/users/<user_id>/edit")
def edit_user(user_id):
    print("$"*50)
    print (request.form)
    mysql = connectToMySQL('new_friends')
    query = "Select * from new_friends.friends where id = {};".format(int(user_id))
    
    
    print(query)
    user_q = mysql.query_db(query)

    return render_template("edit.html", user = user_q)

@app.route("/users/<user_id>/update", methods = ["POST"])
def update_users(user_id):
    print("$"*50)
    print (request.form)
    mysql = connectToMySQL('new_friends')
    query = "UPDATE new_friends.friends SET first_name = %(fname)s, last_name = %(lname)s,  email = %(uemail)s where id={};".format(int(user_id))
    
    data ={
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'uemail': request.form['email']
    }
    print(query)
    user_update = mysql.query_db(query, data)

    return redirect("/users/{}".format(int(user_id)))


@app.route("/users/<user_id>/destroy", methods = ["POST"])
def destroy_users(user_id):
    print("$"*50)
    print (request.form)
    mysql = connectToMySQL('new_friends')
    query = "DELETE From new_friends.friends where id={};".format(int(user_id))
    
    print(query)
    user_delete = mysql.query_db(query)

    return redirect("/users")
   
    

if __name__== "__main__":
    app.run(debug=True)