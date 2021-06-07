import os
import math
import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# Creates instance of Flask
app = Flask(__name__)

# App configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# Instance of PyMongo
# Ensures our Flask app is properly communicating with the Mongo database
mongo = PyMongo(app)


@app.errorhandler(404)
def page_not_found(e):
    # https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# Helper function
def get_pagination_data(number_of_books, page):
    BOOKS_PER_PAGE = 8

    # Gets the number of pages for pagination
    number_of_pages = math.ceil(number_of_books / BOOKS_PER_PAGE)

    # For chevron links
    previous_page = 1
    next_page = number_of_pages

    # Prevents going to page 0
    if page == 0:
        previous_page = 1

    # Prevents going beyond the max number of pages
    if page == number_of_pages:
        next_page = number_of_pages

    # For deciding "active" class
    current_page = int(page)

    pagination_data = {
        "BOOKS_PER_PAGE": BOOKS_PER_PAGE,
        "offset": -1,
        "number_of_pages": number_of_pages,
        "previous_page": previous_page,
        "current_page": current_page,
        "next_page": next_page
    }
    return pagination_data


@app.route("/search", methods=["GET", "POST"])
@app.route("/search/<page>")
def search(page=1):

    # Store query in session
    if request.method == "POST":
        session["query"] = request.form.get("query")

        number_of_books = len(list(mongo.db.books.find({"$text": {"$search": session["query"]}})))

        pagination_data = get_pagination_data(number_of_books, page)

        books = list(mongo.db.books.aggregate([
            {
                "$match": { "$text": { "$search": session["query"] } }
            },
            {
                "$skip": (pagination_data["BOOKS_PER_PAGE"] * (pagination_data["offset"] + int(page)))
            },
            {
                "$limit": pagination_data["BOOKS_PER_PAGE"]
            }
        ]))
        return redirect(url_for("search", page=page))

    if request.method == "GET":
        if session["query"]:
            number_of_books = len(list(mongo.db.books.find({"$text": {"$search": session["query"]}})))
            pagination_data = get_pagination_data(number_of_books, page)
            books = list(mongo.db.books.aggregate([
                {
                    "$match": {"$text": {"$search": session["query"]}}
                },
                {
                    "$skip": (pagination_data["BOOKS_PER_PAGE"] * (pagination_data["offset"] + int(page)))
                },
                {
                    "$limit": pagination_data["BOOKS_PER_PAGE"]
                }
            ]))
            return render_template("books.html", number_of_pages=pagination_data["number_of_pages"], books=books, page=page, next_page=pagination_data["next_page"], previous_page=pagination_data["previous_page"], current_page=pagination_data["current_page"], query_exists=True)

        return render_template("index.html")


@app.route("/books", methods=["GET", "POST"])
@app.route("/books/<page>")
def get_books(page=1):
    # For Search query from Home page
    books = None
    if request.method == "POST":
        query = request.form.get("query")
        books = list(mongo.db.books.find({"$text": {"$search": query}}))

    # Gets the number of books in the books collection
    number_of_books = 0
    if books is None:
        number_of_books = mongo.db.books.estimated_document_count()
    else:
        number_of_books = len(books)

    # Call helper function
    pagination_data = get_pagination_data(number_of_books, page)

    # Retrieve books if there is no search query
    if books is None:
        books = list(mongo.db.books.aggregate([
            {
                "$skip": (pagination_data["BOOKS_PER_PAGE"] * (pagination_data["offset"] + int(page)))
            },
            {
                "$limit": pagination_data["BOOKS_PER_PAGE"]
            }
        ]))

    return render_template("books.html", number_of_pages=pagination_data["number_of_pages"], books=books, page=page, next_page=pagination_data["next_page"], previous_page=pagination_data["previous_page"], current_page=pagination_data["current_page"], query_exists=False)


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
            "rating": int(request.form.get("stars"))
        }
        print(review)
        mongo.db.reviews.insert_one(review)
        flash("Review added!")
        return redirect(url_for("book", book_id=book_id))
    
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

    # reviews = list(mongo.db.reviews.find())
    # reviews = mongo.db.reviews.find_one({"book_id": book_id})
    # db.collection.find({ "fieldToCheck": { $exists: true, $ne: null } })
    
    # https://stackoverflow.com/questions/51244068/pymongo-how-to-check-if-field-exists
    query = {"book_id": {"$eq": book_id}}
    reviews = list(mongo.db.reviews.find(query))

    # Calculate review rating percentage
    total_rating = 0
    for review in reviews:
        total_rating += review["rating"]

    no_of_reviews = len(reviews)
    rating_percentage = 0

    if no_of_reviews > 0:
        rating_average = total_rating / no_of_reviews
        rating_percentage = (rating_average / 5.0) * 100

    return render_template("book.html", book=book, reviews=reviews, no_of_reviews=no_of_reviews, rating=rating_percentage)


# Contact page
@app.route("/contact")
def contact(search=False):
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