import imghdr
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
if os.path.exists("env.py"):
    import env


# Creates instance of Flask
app = Flask(__name__)

# App configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY") # Required for some Flask functions

# Prevents files that are over 1 MB from being uploaded as a Defensive Design feature
# (This relates to uploading the cover image for a book)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

# Validating File Names
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

# Location for uploaded images
app.config['UPLOAD_PATH'] = 'uploads'

# Instance of PyMongo
# Ensures our Flask app is properly communicating with the Mongo database
mongo = PyMongo(app)

# Helper function
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

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

    if request.method == "POST":
        pass

    return render_template("contact.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "is_admin": "No"
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    if request.method == "POST":
        # Create book document for books collection
        book = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "genre": request.form.get("genre"),
            "image": request.form.get("image"),
            "description": request.form.get("description"),
            "uploaded_by": session["user"],
            "rating": 0
        }
        mongo.db.books.insert_one(book)
        flash("Book successfully added to the library!")
        return redirect(url_for("books"))

    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("add-book.html", genres=genres)

# Tells app how and where to host application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)