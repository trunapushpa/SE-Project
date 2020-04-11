from application import app, db
from flask import render_template
import application.dbModels.users
from application.dbModels.users import Users

@app.route("/")
@app.route("/home")
def index():
    return render_template("helloWorld.html")

@app.route("/myitems")
def myitems():
    return render_template("<h1>No items yet</h1>")

@app.route("/uploaditem")
def uploaditem():
    return render_template("<h1>No yet implemented</h1>")

@app.route("/myprofile")
def myprofile():
    return render_template("<h1>No yet implemented</h1>")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")