from flask import Flask, render_template, session, request, redirect
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'very secret'



@app.route("/")
def index():
    
    
    # session['tries'] += 1
    # print("^"*50)
    # print(session['tries'])
    return render_template("index.html")


@app.route("/process_money", methods = ['POST'])
def process_money():
    try:
        session['gold']
    except KeyError:
        session['gold'] = 0
    try:
        session['log']
    except KeyError:
        session['log'] = []
    if "tries" in session:
        session["tries"] += 1
    if request.form["building"]=='farm':
        gold = random.randint(10,20)
    elif request.form['building'] == 'cave':
       gold = random.randint(5,10)
        
    elif request.form['building'] == 'house':
        gold = random.randint(2,5)
       
    elif request.form['building'] == 'casino':
        gold = random.randint(-50,50)
    print("session"*50)
    print(session)
    session['gold'] += gold
    activity =''
    log = ''
   
    time = datetime.now()
    if gold>=0:
        activity = 'Earned ' + str(gold) + ' golds from the ' + str(request.form['building'])
    else:
        activity = 'Entered a casino and lost ' + str(gold) + ' golds... Ouch...' 
    log = activity + '! (' + str(time) + ')'
    session['log'].insert(0,log)
   
    print(session['log'])
    print("^"*50)
    print(session['tries'])
    if session['tries']>15:
        return redirect('/reset')
    
    return redirect("/") 

@app.route('/reset', methods=['get', 'post'])
def reset():
    session["tries"] = 0
    session['gold'] = 0
    session['log'] = []
    return redirect("/") 



if __name__ == "__main__":
    app.run(debug=True)
    