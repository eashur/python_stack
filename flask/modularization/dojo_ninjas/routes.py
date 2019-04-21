from config import app
from controller_functions import index, newdojo, newuser


app.add_url_rule("/", view_func=index)
app.add_url_rule("/add_dojo", view_func=newdojo, methods=["POST"])
app.add_url_rule("/add_ninja", view_func=newuser, methods=["POST"])


# @app.route("/")


# @app.route("/add_dojo", methods =["POST"])


# @app.route("/add_ninja", methods =["POST"])
