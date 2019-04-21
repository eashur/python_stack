from flask import Flask, render_template
app = Flask(__name__) 
@app.route('/<board_size>')


def checker(board_size):
    

    return render_template("index.html", brd_size = int(board_size))

if __name__ =="__main__":
    app.run(debug=True)
