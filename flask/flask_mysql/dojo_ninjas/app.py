from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
from flask_migrate import Migrate 
app = Flask(__name__)

# flask db init
#flask db upgrade

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dojo_ninjas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#instance of the ORM
db =  SQLAlchemy(app)
migrate = Migrate(app, db)
class Dojo(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    city = db.Column(db.String(45))
    State = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Ninja(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    dojo_id = db.Column(db.Integer, db.ForeignKey("dojo.id"), nullable = False)
    dojo = db.relationship('Dojo', foreign_keys=[dojo_id], backref="dojo_ninjas", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

@app.route("/")
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

@app.route("/add_dojo", methods =["POST"])
def newdojo():
   
    new_instance_of_a_dojo = Dojo(name=request.form['name'], \
        city=request.form['city'], State=request.form['state'])
    db.session.add(new_instance_of_a_dojo)
    db.session.commit()

    return redirect("/")

@app.route("/add_ninja", methods =["POST"])
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




if __name__== "__main__":
    app.run(debug=True)