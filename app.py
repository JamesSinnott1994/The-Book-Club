import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


# Creates instance of Flask
app = Flask(__name__)

# App configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY") # Required for some Flask functions

# Instance of PyMongo
# Ensures our Flask app is properly communicating with the Mongo database
mongo = PyMongo(app)

# Default root
# Home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Books page
@app.route("/books")
def books():
    return render_template("books.html")


# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Login page
@app.route("/login")
def login():
    return render_template("login.html")


# Register page
@app.route("/register")
def register():
    return render_template("register.html")


# Tells app how and where to host application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)