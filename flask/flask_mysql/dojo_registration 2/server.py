from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=\S{5,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

@app.route("/")
def index():

    return render_template("registration.html")

@app.route("/register", methods = ["POST"])
def register_user():
    print("regitering a user")
    session["fname"] = request.form['first_name']

    is_valid = True		# assume True
    if not (len(request.form['first_name']) > 0  
        and
        request.form['first_name'].isalpha()):
        is_valid = False
        flash("Please enter valid first name")
        print("Please enter first name")
        
    
    if not (len(request.form['last_name']) >0 
        and
        request.form['last_name'].isalpha()):
        is_valid = False
        flash("Please enter valid last name")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    if not PW_REGEX.match(request.form['password']):
        is_valid = False
        flash("Please enter valid password, password should be at least 5 chars, contain at least one upper case letter, lower case letter special char and number")
    # if len(request.form['password']) < 5:
    #     is_valid = False
    #     flash("Please enter valid password, password should be at least 5 chars")
    
    if (request.form['password']!=request.form['cpassword']):
        is_valid = False
        flash("Confirm password should match the password")

    if is_valid:
        flash("Successfully Registered!")
        print("Successfully Registered!")

        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        print(pw_hash) 
        mysql = connectToMySQL('twitter')
        query = "INSERT INTO twitter.users (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(em)s, %(pw)s);"
    
        data ={
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'em': request.form['email'],
        'pw': pw_hash
         }
        print(query)
        add_data = mysql.query_db(query, data)
        print(add_data)
        print("**"*25)

        return redirect('/success')
    return redirect('/')

@app.route("/success")
def success():
    tw_authors = []
    # for i in range(len(session['result'])):
    #     mysql = connectToMySQL("twitter")
    #     query = f"SELECT first_name, last_name FROM twitter.users WHERE id = {session['result'][i]['user_id']};"
    #     author = mysql.query_db(query)
    #     tw_authors.append(author)
    # print(tw_authors) authors = tw_authors
    # print('^'*45)



    return render_template("success.html", name = session["fname"], results = session['result'])

@app.route("/login", methods = ["POST"])
def login():

    session["fname"]= ''
    session['userid'] = ''

    mysql = connectToMySQL("twitter")
    query = "SELECT * FROM twitter.users WHERE email = %(username)s;"
    data = { "username" : request.form["username"] }
    result = mysql.query_db(query, data)
    if result:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            # if we get True after checking the password, we may put the user id in session
            session['userid'] = result[0]['id']
            # never render on a post, always redirect!
            flash("Successfully Logged in!")
            session["fname"] = result[0]['first_name']
            return redirect('/success')
    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # flash an error message and redirect back to a safe route
    flash("You could not be logged in")
    return redirect("/")

@app.route("/process", methods = ["POST"])
def process_tweet():
    is_valid = True	
     
    if not (len(request.form['ttext']) >0 
        and
        (len(request.form['ttext']) < 255)):
        is_valid = False
        flash("Please enter valid tweet")
        return redirect('/success')
     
    if is_valid:
        mysql = connectToMySQL("twitter")
        query = "INSERT INTO twitter.tweets (tweet, user_id) VALUES (%(twtext)s, %(uid)s);"
        
        data = { 
            'twtext' : request.form['ttext'],
            'uid': session['userid'],
            }
        new_tweet = mysql.query_db(query, data)


        mysql = connectToMySQL("twitter")
        query = "SELECT twitter.tweets.tweet, twitter.tweets.created_at, twitter.users.first_name, twitter.users.last_name FROM twitter.tweets JOIN twitter.users ON twitter.tweets.user_id = twitter.users.id;"
        session['result'] = mysql.query_db(query)
        print(session['result'])
        print('#'*45)

        return redirect('/success')

    

if __name__== "__main__":
    app.run(debug=True)