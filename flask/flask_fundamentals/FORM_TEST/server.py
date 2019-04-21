from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'very secret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods = ["POST"])
def process_form():
    print("in the process_form function")
    print("*"*50)
    print(request.form)
    session['username'] = request.form['username']
    session['useremail'] = request.form['email']
    print(f"Username submitted: {request.form['username']}")
    print(f"Email submitted: {request.form['email']}")

    return redirect("/show")

@app.route("/show")
def show_user():

    print ("just showing the user")


    return render_template("info.html", 
    name =session["username"], em= session["useremail"])

if __name__ == "__main__":
    app.run(debug=True)


