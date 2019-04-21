from config import app
from controller_functions import index, add_newuser, login, logout, follow


app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=add_newuser, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/follow", view_func=follow, methods=["POST"])
app.add_url_rule("/", view_func=logout)

