from flask import Flask, render_template
app = Flask(__name__) 
@app.route('/play/<times>/<color>')


def playground(times, color):
    

    return render_template("index.html", num_times = int(times), col= color)

if __name__ =="__main__":
    app.run(debug=True)
