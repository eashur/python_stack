from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

@app.route('/')
def index():
    option_list = ['', 'San Jose', 'New York', 'Seattle']
    language_list = ['', 'Python', 'PHP', 'Javascript']
    return render_template('index.html', option_list=option_list, language_list=language_list)

@app.route('/create', methods=['POST'])
def create_user():
    print("creating a user")

    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['language'] = request.form['language']
    session['comment'] = request.form['comment']
    
    is_valid = True		# assume True
    if len(request.form['name']) < 1:
        is_valid = False
        flash("Please enter a first name")
        print("Please enter a first name")
    
    if len(request.form['location']) < 1:
        is_valid = False
        flash("Please choose your location")

    if len(request.form['language']) < 1:
        is_valid = False
        flash("Please choose your favorite language")

    if len(request.form['comment'])== 0 or len(request.form['comment']) > 120:
        is_valid = False
        flash("Comment should be empty or longer than 120 chars")
        print("Comment should be empty or longer than 120 chars")
    if is_valid:
        flash("Survey Respose Accepted!")
        print("Survey Respose Accepted!")

        mysql = connectToMySQL('new_friends')
        query = "INSERT INTO survey_data.survey (name, dojo_location, favorite_language, comment) VALUES (%(fname)s, %(locat)s, %(flan)s, %(comm)s);"
    
        data ={
        'fname': request.form['name'],
        'locat': request.form['location'],
        'flan': request.form['language'],
        'comm': request.form['comment']
         }
        print(query)
        add_data = mysql.query_db(query, data)
        print(add_data)
        print("**"*25)
    return redirect('/process')

@app.route('/process')
def show_user():


    return render_template('result.html')

if __name__ =="__main__":
    app.run(debug=True)
