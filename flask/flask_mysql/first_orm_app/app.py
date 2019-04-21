from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
from flask_migrate import Migrate 
app = Flask(__name__)

# flask db init
#flask db upgrade

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#instance of the ORM
db =  SQLAlchemy(app)
migrate = Migrate(app, db)
class User(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    age = db.Column(db.String(45))
    password = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

@app.route("/users")
def index():
    list_of_all_users_as_user_instances = User.query.all()

    return render_template("users.html", users= list_of_all_users_as_user_instances)


@app.route("/users/new", methods =["POST"])
def newuser():
    new_instance_of_a_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'], age=request.form['age'],password="abc123")
    db.session.add(new_instance_of_a_user)
    db.session.commit()

    return redirect("/users")

# new_instance_of_a_user = User(first_name="Clark", last_name="Donavan", email="cdon@harper.com", age="36",password="abc123")
# db.session.add(new_instance_of_a_user)
# db.session.commit()


# new_instance_of_a_user = User(first_name="Clark", last_name="Frances", email="frac@harper.com", password="abc123")
# db.session.add(new_instance_of_a_user)
# db.session.commit()

# user_instance_to_delete = User.query.get(15)
# db.session.delete(user_instance_to_delete)
# db.session.commit()







if __name__== "__main__":
    app.run(debug=True)