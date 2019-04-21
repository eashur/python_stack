from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)
@app.route("/")
def index():
    # mysql = connectToMySQL('first_flask')
    # friends = mysql.query_db('Select * From friends;')
   
    mysql = connectToMySQL('first_flask')
    # friends = mysql.query_db('INSERT INTO `first_flask`.`friends` (`first_name`, `last_name`, `occupation`, `created_at`) VALUES ("Bob", "Martin", "sales", now());')
    friends = mysql.query_db('SELECT * FROM first_flask.friends;')
   
    print(friends)

    return render_template("index.html", all_friends = friends)


@app.route("/create_friend", methods =["POST"])
def add_friends_to_db():
    print(request.form)

    mysql = connectToMySQL("first_flask")

    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());"
    data = {
        'fn': request.form['fname'],
        'ln': request.form['lname'],
        'occup': request.form['occ']
    }
    new_friend_id = mysql.query_db(query, data)

    return redirect("/")


if __name__== "__main__":
    app.run(debug=True)
