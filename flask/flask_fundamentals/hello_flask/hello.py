from flask import Flask, render_template # Import Flask to allow us to create our app

app = Flask(__name__)    # Create a new instance of the Flask class called "app"
@app.route('/')          # The "@" decorator associates this route with the function immediately following
def hello_world():
    return render_template("index.html", phrase = "that is cool", times =5)  # Return the string 'Hello World!' as a response

@app.route('/eldor')
def hello_eldor():
    return "Hello Eldor!"

@app.route('/<name>')
def hello_namne(name):
    print("in hello name funtion")
    print(name)
    return "Hello " + name.capitalize()
    



if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    copy
    app.run(debug=True)   # Run the app in debug mode
