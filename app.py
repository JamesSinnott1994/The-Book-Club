import imghdr
import os
import math
import datetime
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


@app.errorhandler(404)
def page_not_found(e):
    # https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# Default root
# Home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Books page
@app.route("/books")
@app.route("/books/<page>")
def books(page=1):
    # 1.
    # Gets the number of books in the books collection
    number_of_books = mongo.db.books.estimated_document_count()

    # Books per page
    BOOKS_PER_PAGE = 8

    # For going through pages
    offset = -1

    # Gets the number of pages for pagination
    number_of_pages = math.ceil(number_of_books / BOOKS_PER_PAGE)

    # For chevron links
    previous_page = 1
    next_page = number_of_pages

    if page == 0:  # Prevents going to page 0
        previous_page = 1
    
    if page == number_of_pages:  # Prevents going beyond the max number of pages
        next_page = number_of_pages

    # For deciding "active" class
    current_page = int(page)

    # Retrieve books
    books = list(mongo.db.books.aggregate([
        {
            "$skip": (BOOKS_PER_PAGE * (offset + int(page)))
        },
        {
            "$limit": BOOKS_PER_PAGE
        }
    ]))

    return render_template("books.html", number_of_pages=number_of_pages, books=books, page=page, next_page=next_page, previous_page=previous_page, current_page=current_page)


@app.route("/book/<book_id>", methods=["GET", "POST"])
def book(book_id):

    if request.method == "POST":
        # Add Review
        review = {
            "title": request.form.get("title"),
            "comment": request.form.get("comment"),
            "book_id": book_id,
            "reviewed_by": session["user"],
            "review_date": datetime.datetime.now().strftime("%d-%m-%Y"),
            "rating": 3
        }
        mongo.db.reviews.insert_one(review)
        flash("Review added!")
        return redirect(url_for("book", book_id=book_id))
    
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    # reviews = list(mongo.db.reviews.find())
    # reviews = mongo.db.reviews.find_one({"book_id": book_id})
    # db.collection.find({ "fieldToCheck": { $exists: true, $ne: null } })
    # reviews = mongo.db.reviews.find({ "book_id": {"$exists": True, "$ne": None }})

    # https://stackoverflow.com/questions/51244068/pymongo-how-to-check-if-field-exists
    query = {"book_id": {"$eq": book_id}}
    reviews = list(mongo.db.reviews.find(query))

    return render_template("book.html", book=book, reviews=reviews)


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


@app.route("/edit_book/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if request.method == "POST":
        updated_book = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "genre": request.form.get("genre"),
            "image": request.form.get("image"),
            "description": request.form.get("description"),
            "uploaded_by": session["user"],
            "rating": 0
        }
        mongo.db.books.update({"_id": ObjectId(book_id)}, updated_book)
        flash("Book Successfully Updated")
        return redirect(url_for("book", book_id=book_id))

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("edit-book.html", book=book, genres=genres)


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    mongo.db.books.remove({"_id": ObjectId(book_id)})

    # Delete all reviews associated with the book
    query = {"book_id": {"$eq": book_id}}
    mongo.db.reviews.remove(query)

    flash("Book Successfully Deleted")
    return redirect(url_for("books"))

# Tells app how and where to host application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)