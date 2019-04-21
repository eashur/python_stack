from flask import Flask, render_template, redirect, session
app = Flask(__name__)
app.secret_key = 'ABCDE'


@app.route('/')
def index():
    if "visits" in session:
	    session["visits"] += 1
    else:
	    session["visits"] = 1
    return render_template('index.html', count=session["visits"])


@app.route('/increment', methods=['POST'])
def increment_by_two():
    session["visits"] += 1
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    session.clear()
    return redirect('/')


if __name__ =="__main__":
    app.run(debug=True)
