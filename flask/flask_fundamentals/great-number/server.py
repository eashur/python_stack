from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)  
app.secret_key = 'ABCDE'

@app.route("/")
def index():
    session["num"] = random.randint(1, 100)
    return render_template("index.html")

@app.route("/process", methods = ["POST"])
def process_submission():
    
    print("*"*50)
    print(session["num"])
    session["message"] = ''
    
    session['guess'] = request.form['guess']

    print(session['guess'])
    if session['guess'].isdigit():
        guess_num = int(session['guess'])
        if guess_num==session["num"]:
            session["message"] = " was the number!!"
            return redirect("/correct")
        elif guess_num>session["num"]:
            session["message"] = "Too High!!"
            return redirect("/wrong")
        elif guess_num<session["num"]:
            session["message"] = "Too Low!!"
            return redirect("/wrong")
    else:
        session["message"] = "Invalid Entry!!"
        return redirect("/wrong")



@app.route("/wrong")
def wrong_guess():
    if "visits" in session:
        session["visits"] += 1
        print(session["visits"])
    else:
	    session["visits"] = 1

    if (session["visits"] >= 5):
        print('LOOOOOOOOOOOzeeeeeeer')
        session["message"] = "You Lose :-( !!"
        session["visits"] = 0
        return render_template("lost.html")

    return render_template("wrong.html")
@app.route("/correct")
def correct_guess():
    return render_template("correct.html")

@app.route("/reset", methods=['GET', 'POST'])
def reset_game():
    session["visits"] = 0
    session["num"] = random.randint(1, 100)
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)