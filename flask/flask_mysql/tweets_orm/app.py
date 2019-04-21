from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=\S{5,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
# flask db init
#flask db upgrade
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tweets_orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =  SQLAlchemy(app)
migrate = Migrate(app, db)

twitter = db.Table('twitter',
    db.Column('users_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=True),
    db.Column('tweets_id', db.Integer, db.ForeignKey('tweets.id'), primary_key=True, nullable=True)) 

follows = db.Table('follows',
   
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=True)
    ) 


class User(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    age = db.Column(db.String(45))
    password = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())   
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    tweets_of_user = db.relationship('Tweets', secondary=twitter, backref='user_tweets', cascade='all')
    follows_of_user =  db.relationship(
        'User', secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.followed_id == id),
        backref='follows', cascade='all')

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())  
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())    
    user_who_tweeted = db.relationship('User', secondary=twitter, backref='tweet_from_user', cascade='all')


@app.route("/")
def reg():
    session["fname"]= ''
    session['userid'] = ''

    return render_template("registration.html")

@app.route("/users")
def index():
    list_of_all_users_as_user_instances = User.query.all()

    return render_template("users.html", users= list_of_all_users_as_user_instances)


@app.route("/register", methods =["POST"])
def newuser():
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
        flash("Successfully Registered! Please Log In")
        print("Successfully Registered!")

        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        print(pw_hash) 
    new_instance_of_a_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'], age=request.form['age'],password=pw_hash)
    db.session.add(new_instance_of_a_user)
    db.session.commit()

    return redirect("/")



@app.route("/login", methods = ["POST"])
def login():
    if len(request.form['username'])<5: 
        flash("Please enter email")
        return redirect('/')
    if len(request.form['password'])<1: 
        flash("Please enter password")
        return redirect('/')

    session["fname"]= ''
    session['userid'] = ''

    
    result = User.query.filter_by(email = request.form["username"]).first()
    if result:
       
        if bcrypt.check_password_hash(result.password, request.form['password']):
            session['userid'] = result.id
            flash("Successfully Logged in!")
            session["fname"] = result.first_name
            return redirect('/success')
    flash("You could not be logged in")
    return redirect("/")


@app.route("/success")
def success():
    session['result'] = []


    # mysql = connectToMySQL("twitter")
    # query = "SELECT twitter.follows.id, twitter.users.first_name, twitter.users.last_name, twitter.users.email  FROM twitter.follows \
    #     JOIN twitter.users on twitter.follows.followed_id = twitter.users.id\
    #     WHERE twitter.follows.follower_id = %(uid)s;"
    # data = { 
    #     'uid': session['userid'],
        
    #     }
    # session['follow_list'] = mysql.query_db(query, data)
    # if (len(session['follow_list'])==0):
    #     flash("You are not following anyone, please start following someone to see a list of tweets")



    # print(session['follow_list'])
    # mysql = connectToMySQL("twitter")
    # query = f"SELECT tt.id, tu.first_name, tu.last_name, tt.created_at, tt.tweet, tt.user_id,  twitter.follows.id as follow_id, \
    #             twitter.follows.followed_id, twitter.follows.follower_id \
    #             FROM twitter.tweets \
    #             LEFT JOIN twitter.users on twitter.tweets.user_id = twitter.users.id \
    #             LEFT JOIN twitter.follows on twitter.tweets.user_id = twitter.follows.follower_id \
    #             JOIN twitter.tweets AS tt  on twitter.follows.followed_id=tt.user_id \
    #             JOIN twitter.users as tu on tu.id = tt.user_id \
    #             WHERE twitter.follows.follower_id= {session['userid']} or tt.user_id ={session['userid']};"
    # session['result'] = mysql.query_db(query)
    # session['result'] = db.session.query(User, Tweets).join(Tweets, User.tweets_of_user).all()
    session['result'] =  Tweets.query.join(
            follows, (follows.c.followed_id == Tweets.user_who_tweeted)).filter(
                follows.c.follower_id == session['userid']).order_by(
                    Tweets.created_at.desc())
    print(session['result'])
   

    return render_template("success.html", name = session["fname"], results = session['result'], following = session['follow_list'])


@app.route("/process", methods = ["POST"])
def process_tweet():
    is_valid = True
    session['result'] = []
     
    if not (len(request.form['ttext']) >0 
        and
        (len(request.form['ttext']) < 255)):
        is_valid = False
        flash("Please enter valid tweet")
        return redirect('/success')
     
    if is_valid:
        # mysql = connectToMySQL("twitter")
        # query = "INSERT INTO twitter.tweets (tweet, user_id) VALUES (%(twtext)s, %(uid)s);"
        
        # data = { 
        #     'twtext' : request.form['ttext'],
        #     'uid': session['userid'],
        #     }
        new_tweet = Tweets(content = request.form['ttext'])
        db.session.add(new_tweet)
        db.session.commit()


        # mysql = connectToMySQL("twitter")
        # # query = "SELECT twitter.tweets.id,twitter.tweets.tweet, twitter.tweets.created_at, twitter.users.first_name, twitter.users.last_name FROM twitter.tweets JOIN twitter.users ON twitter.tweets.user_id = twitter.users.id;"
        # query = f"SELECT tt.id, tu.first_name, tu.last_name, tt.created_at, tt.tweet, tt.user_id,  twitter.follows.id as follow_id, \
        #         twitter.follows.followed_id, twitter.follows.follower_id \
        #         FROM twitter.tweets \
        #         LEFT JOIN twitter.users on twitter.tweets.user_id = twitter.users.id \
        #         LEFT JOIN twitter.follows on twitter.tweets.user_id = twitter.follows.follower_id \
        #         RIGHT JOIN twitter.tweets AS tt  on twitter.follows.followed_id=tt.user_id \
        #         JOIN twitter.users as tu on tu.id = tt.user_id \
        #         WHERE twitter.follows.follower_id= {session['userid']} or tt.user_id ={session['userid']};"
        # session['result'] = mysql.query_db(query)
        # print(session['result'])
        print('#'*45)

        return redirect('/success')


# new_instance_of_a_user = User(first_name="Clark", last_name="Donavan", email="cdon@harper.com", age="36",password="abc123")
# db.session.add(new_instance_of_a_user)
# db.session.commit()


# new_instance_of_a_user = User(first_name="Clark", last_name="Frances", email="frac@harper.com", password="abc123")
# db.session.add(new_instance_of_a_user)
# db.session.commit()

# user_instance_to_delete = User.query.get(15)
# db.session.delete(user_instance_to_delete)
# db.session.commit()



# @app.route("/register", methods = ["POST"])
# def register_user():
#     print("regitering a user")
#     session["fname"] = request.form['first_name']

#     is_valid = True		# assume True
#     if not (len(request.form['first_name']) > 0  
#         and
#         request.form['first_name'].isalpha()):
#         is_valid = False
#         flash("Please enter valid first name")
#         print("Please enter first name")
        
    
#     if not (len(request.form['last_name']) >0 
#         and
#         request.form['last_name'].isalpha()):
#         is_valid = False
#         flash("Please enter valid last name")
#     if not EMAIL_REGEX.match(request.form['email']):
#         is_valid = False
#         flash("Invalid email address!")
#     if not PW_REGEX.match(request.form['password']):
#         is_valid = False
#         flash("Please enter valid password, password should be at least 5 chars, contain at least one upper case letter, lower case letter special char and number")
#     # if len(request.form['password']) < 5:
#     #     is_valid = False
#     #     flash("Please enter valid password, password should be at least 5 chars")
    
#     if (request.form['password']!=request.form['cpassword']):
#         is_valid = False
#         flash("Confirm password should match the password")

#     if is_valid:
#         flash("Successfully Registered! Please Log In")
#         print("Successfully Registered!")

#         pw_hash = bcrypt.generate_password_hash(request.form['password'])  
#         print(pw_hash) 
#         mysql = connectToMySQL('twitter')
#         query = "INSERT INTO twitter.users (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(em)s, %(pw)s);"
    
#         data ={
#         'fname': request.form['first_name'],
#         'lname': request.form['last_name'],
#         'em': request.form['email'],
#         'pw': pw_hash
#          }
#         print(query)
#         add_data = mysql.query_db(query, data)
#         print(add_data)
#         print("**"*25)

#         return redirect('/')
#     return redirect('/')

# @app.route("/success")
# def success():
#     session['result'] = []
#     mysql = connectToMySQL("twitter")
#     query = "SELECT twitter.follows.id, twitter.users.first_name, twitter.users.last_name, twitter.users.email  FROM twitter.follows \
#         JOIN twitter.users on twitter.follows.followed_id = twitter.users.id\
#         WHERE twitter.follows.follower_id = %(uid)s;"
#     data = { 
#         'uid': session['userid'],
        
#         }
#     session['follow_list'] = mysql.query_db(query, data)
#     if (len(session['follow_list'])==0):
#         flash("You are not following anyone, please start following someone to see a list of tweets")



#     print(session['follow_list'])
#     mysql = connectToMySQL("twitter")
#     query = f"SELECT tt.id, tu.first_name, tu.last_name, tt.created_at, tt.tweet, tt.user_id,  twitter.follows.id as follow_id, \
#                 twitter.follows.followed_id, twitter.follows.follower_id \
#                 FROM twitter.tweets \
#                 LEFT JOIN twitter.users on twitter.tweets.user_id = twitter.users.id \
#                 LEFT JOIN twitter.follows on twitter.tweets.user_id = twitter.follows.follower_id \
#                 JOIN twitter.tweets AS tt  on twitter.follows.followed_id=tt.user_id \
#                 JOIN twitter.users as tu on tu.id = tt.user_id \
#                 WHERE twitter.follows.follower_id= {session['userid']} or tt.user_id ={session['userid']};"
#     session['result'] = mysql.query_db(query)
#     print(session['result'])

#     return render_template("success.html", name = session["fname"], results = session['result'], following = session['follow_list'])

# @app.route("/login", methods = ["POST"])
# def login():

#     session["fname"]= ''
#     session['userid'] = ''

#     mysql = connectToMySQL("twitter")
#     query = "SELECT * FROM twitter.users WHERE email = %(username)s;"
#     data = { "username" : request.form["username"] }
#     result = mysql.query_db(query, data)
#     if result:
#         # assuming we only have one user with this username, the user would be first in the list we get back
#         # of course, we should have some logic to prevent duplicates of usernames when we create users
#         # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
#         if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
#             # if we get True after checking the password, we may put the user id in session
#             session['userid'] = result[0]['id']
#             # never render on a post, always redirect!
#             flash("Successfully Logged in!")
#             session["fname"] = result[0]['first_name']
#             return redirect('/success')
#     # if we didn't find anything in the database by searching by username or if the passwords don't match,
#     # flash an error message and redirect back to a safe route
#     flash("You could not be logged in")
#     return redirect("/")

# @app.route("/process", methods = ["POST"])
# def process_tweet():
#     is_valid = True
#     session['result'] = []
     
#     if not (len(request.form['ttext']) >0 
#         and
#         (len(request.form['ttext']) < 255)):
#         is_valid = False
#         flash("Please enter valid tweet")
#         return redirect('/success')
     
#     if is_valid:
#         mysql = connectToMySQL("twitter")
#         query = "INSERT INTO twitter.tweets (tweet, user_id) VALUES (%(twtext)s, %(uid)s);"
        
#         data = { 
#             'twtext' : request.form['ttext'],
#             'uid': session['userid'],
#             }
#         new_tweet = mysql.query_db(query, data)


#         # mysql = connectToMySQL("twitter")
#         # # query = "SELECT twitter.tweets.id,twitter.tweets.tweet, twitter.tweets.created_at, twitter.users.first_name, twitter.users.last_name FROM twitter.tweets JOIN twitter.users ON twitter.tweets.user_id = twitter.users.id;"
#         # query = f"SELECT tt.id, tu.first_name, tu.last_name, tt.created_at, tt.tweet, tt.user_id,  twitter.follows.id as follow_id, \
#         #         twitter.follows.followed_id, twitter.follows.follower_id \
#         #         FROM twitter.tweets \
#         #         LEFT JOIN twitter.users on twitter.tweets.user_id = twitter.users.id \
#         #         LEFT JOIN twitter.follows on twitter.tweets.user_id = twitter.follows.follower_id \
#         #         RIGHT JOIN twitter.tweets AS tt  on twitter.follows.followed_id=tt.user_id \
#         #         JOIN twitter.users as tu on tu.id = tt.user_id \
#         #         WHERE twitter.follows.follower_id= {session['userid']} or tt.user_id ={session['userid']};"
#         # session['result'] = mysql.query_db(query)
#         # print(session['result'])
#         print('#'*45)

#         return redirect('/success')

    

# @app.route("/like", methods = ["POST"])
# def like_tweet():

#     mysql = connectToMySQL("twitter")
#     query = "SELECT twitter.faves.user_id FROM twitter.faves WHERE twitter.faves.user_id = %(uid)s AND twitter.faves.tweet_id = %(twid)s;"
#     data = { 
#         'uid': session['userid'],
#         'twid' : request.form['which_tweet']
#         }
#     new_tweet_id = mysql.query_db(query, data)
#     print(new_tweet_id)

#     if (len(new_tweet_id)==0):
#         mysql = connectToMySQL("twitter")
#         query = "INSERT INTO twitter.faves (user_id, tweet_id) VALUES (%(uid)s, %(twid)s );"
#         data = { 
#             'uid': session['userid'],
#             'twid' : request.form['which_tweet']
#             }
#         print(request.stream.read())
#         print('-'*45)
#         new_tweet = mysql.query_db(query, data)
#         print(query)
#         return redirect('/success')

#     flash("You have already liked this tweet")
#     return redirect('/success')


@app.route("/delete", methods = ["POST"])
def delete_tweet():
    # session['result'] = []
    # mysql = connectToMySQL("twitter")

    # query = "DELETE FROM twitter.tweets WHERE id = %(twid)s;"
    # data = { 
        
    #     'twid' : request.form['which_tweet']
    #     }
    # new_tweet_id = mysql.query_db(query, data)
    # print(new_tweet_id)
    # print(query)

    # mysql = connectToMySQL("twitter")
    # query = "SELECT twitter.tweets.id,twitter.tweets.tweet, twitter.tweets.created_at, twitter.users.first_name, twitter.users.last_name FROM twitter.tweets JOIN twitter.users ON twitter.tweets.user_id = twitter.users.id;"
    # session['result'] = mysql.query_db(query)
    # print(session['result'])
    # print('#'*45)
    flash("Successfully deleted tweet")
    return redirect('/success')
    
@app.route("/cancel_edit", methods = ["POST"])
def cancel_edit_tweet():
    # session['result'] = []
    # mysql = connectToMySQL("twitter")
    # query = "SELECT twitter.tweets.id,twitter.tweets.tweet, twitter.tweets.created_at, twitter.users.first_name, twitter.users.last_name FROM twitter.tweets JOIN twitter.users ON twitter.tweets.user_id = twitter.users.id;"
    # session['result'] = mysql.query_db(query)
    # print(session['result'])
    # print('#'*45)
    # flash("Successfully deleted tweet")
    return redirect('/success')

@app.route("/edit", methods = ["POST"])
def submit_edit_tweet():
    # is_valid = True
    # session['result'] = []
    # tw_id = request.form['which_tweet']
     
    # if not (len(request.form['utext']) >0 
    #     and
    #     (len(request.form['utext']) < 255)):
    #     is_valid = False
        flash("Please enter valid tweet")

        return redirect(f'/{tw_id}/edit')

    # mysql = connectToMySQL("twitter")
    # query = "UPDATE twitter.tweets SET `tweet` = %(text)s WHERE id =%(twid)s;"
 
    # data = { 
    #     'text': request.form['utext'],
    #     'twid' : request.form['which_tweet']
    #     }
    # updated_tweet = mysql.query_db(query, data)

    # mysql = connectToMySQL("twitter")
    # query = "SELECT twitter.tweets.id,twitter.tweets.tweet, twitter.tweets.created_at, twitter.users.first_name, twitter.users.last_name FROM twitter.tweets JOIN twitter.users ON twitter.tweets.user_id = twitter.users.id;"
    # session['result'] = mysql.query_db(query)
    # print(session['result'])
    # print('#'*45)
    flash("Successfully deleted tweet")
    return redirect('/success')


@app.route("/<tw_id>/edit", methods = ["GET","POST"])
def edit_tweet(tw_id):
    session['result'] = []
    mysql = connectToMySQL("twitter")
    query = f"SELECT twitter.tweets.id,twitter.tweets.tweet FROM twitter.tweets WHERE id = {tw_id};"
    session['result'] = mysql.query_db(query)
    print(session['result'])
    print('#'*45)
    flash("Editing tweet")
    return render_template('edit.html', result = session['result'] )


# @app.route("/users", methods = ["GET"])
# def users_dashboard():
#     session['user_list'] = []
#     mysql = connectToMySQL("twitter")
#     query = "SELECT twitter.users.id, twitter.users.first_name, twitter.users.last_name, twitter.users.email FROM twitter.users;"
#     session['user_list'] = mysql.query_db(query)
#     print(session['result'])
#     print('#'*45)
#     flash(" ")
#     return render_template('users.html', users = session['user_list'] )

# @app.route("/follow", methods = ["POST"])
# def follow_user():

#     mysql = connectToMySQL("twitter")
#     query = "SELECT * FROM twitter.follows WHERE twitter.follows.follower_id = %(uid)s AND twitter.follows.followed_id = %(fwid)s;"
#     data = { 
#         'uid': session['userid'],
#         'fwid' : request.form['followed_id']
#         }
#     follow_list = mysql.query_db(query, data)
#     print(follow_list)

#     if (len(follow_list)==0):
#         mysql = connectToMySQL("twitter")
#         query = "INSERT INTO twitter.follows (follower_id, followed_id) VALUES (%(uid)s, %(fwid)s );"
#         data = { 
#             'uid': session['userid'],
#             'fwid' : request.form['followed_id']
#             }
#         print(request.stream.read())
#         print('-'*45)
#         new_follow = mysql.query_db(query, data)
#         print(query)
#         return redirect('/users')

#     flash("You are already following this user")
#     return redirect('/users')






if __name__== "__main__":
    app.run(debug=True)