from flask import Flask, redirect
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dojo')
def hello_dojo():
    return 'Dojo!'

@app.route('/say/<name>')
def hello_name(name):
    return "Hi " + name.capitalize()

@app.route('/repeat/<num>/<mess>')
def repeat_mess(num, mess):
    repeating = []
    for i in range(int(num)+1):
        repeating.append(mess)
        print('<><><>><><><><><>'+mess)
    
    return ", ".join(repeating)


if __name__ =="__main__":
    app.run(debug=True)
