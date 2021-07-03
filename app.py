import os
import math
import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from bson.objectid import ObjectId
from smtplib import SMTPException
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# Creates instance of Flask
app = Flask(__name__)

# App configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")

# Instance of PyMongo
# Ensures our Flask app is properly communicating with the Mongo database
mongo = PyMongo(app)

# Flask Mail
mail = Mail(app)


@app.errorhandler(500)
def internal_error(e):
    """Returns template for the 500 Error page"""
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    """Returns template for the 404 Error page"""

    # https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route("/")
@app.route("/home")
def home():
    """Returns template for Home page"""

    # Get the top 4 most popular books in order of total_rating
    books = list(mongo.db.books.find(
        {
            "$query": {},
            "$orderby": {"total_rating": -1}
        }).limit(4)
    )

    return render_template("index.html", books=books)


@app.route("/search", methods=["GET", "POST"])
@app.route("/search/<page>")
def search(page=1):
    """
    1. If user submits a query, find books associated
    with query.

    - User is then redirected to this search route
    (Helps get rid of an issue with the URL)

    2. Retrieves submitted query

    - If there are no results from the query, then
    a message will be displayed in template based on
    the "results" boolean
    """

    # 1. store submitted query in session
    if request.method == "POST":
        session["query"] = request.form.get("query")
        return redirect(url_for("search", page=page))

    # 2. retrieve submitted query which is stored in session
    if request.method == "GET":
        if session["query"]:
            number_of_books = len(list(mongo.db.books.find(
                {
                    "$text": {"$search": session["query"]}
                }
            )))

            pagination_data = get_pagination_data(number_of_books, page)

            books = list(mongo.db.books.aggregate([
                {
                    "$match": {"$text": {"$search": session["query"]}}
                },
                {
                    "$skip": (
                        pagination_data["BOOKS_PER_PAGE"] *
                        (pagination_data["offset"] + int(page))
                    )
                },
                {
                    "$limit": pagination_data["BOOKS_PER_PAGE"]
                }
            ]))

            # determines if there are any results to be displayed
            # from query.
            results = True
            if number_of_books == 0:
                results = False

            return render_template(
                "books.html",
                number_of_pages=pagination_data["number_of_pages"],
                books=books, page=page, next_page=pagination_data["next_page"],
                previous_page=pagination_data["previous_page"],
                current_page=pagination_data["current_page"],
                query_exists=True, results=results
            )

        return render_template("index.html")


@app.route("/books", methods=["GET", "POST"])
@app.route("/books/<page>")
def get_books(page=1):
    """
    Returns template for the Books page

    - "books" will hold either books based on a search query,
    or it will hold all books from the books collection.

    - Initially it is set to "None", this is to accomodate a
    search query from the user.

    - If there is no POST request, then that means there was no
    search query. "books" will therefore be "None", so all books are
    then retrieved from the database.
    """

    books = None  # default value

    # for search query from Home page
    if request.method == "POST":
        query = request.form.get("query")
        books = list(mongo.db.books.find({"$text": {"$search": query}}))

    # gets the number of books
    number_of_books = 0
    if books is None:  # calculate number of books in database
        number_of_books = mongo.db.books.estimated_document_count()
    else:  # get number of books retrieved from search query
        number_of_books = len(books)

    # call helper function
    pagination_data = get_pagination_data(number_of_books, page)

    # retrieve books if there is no search query
    if books is None:
        books = list(mongo.db.books.aggregate([
            {
                "$skip": (
                    pagination_data["BOOKS_PER_PAGE"] *
                    (pagination_data["offset"] + int(page))
                )
            },
            {
                "$limit": pagination_data["BOOKS_PER_PAGE"]
            }
        ]))

    return render_template(
        "books.html",
        number_of_pages=pagination_data["number_of_pages"],
        books=books, page=page, next_page=pagination_data["next_page"],
        previous_page=pagination_data["previous_page"],
        current_page=pagination_data["current_page"],
        query_exists=False, results=True
    )


def get_pagination_data(number_of_books, page):
    """
    Helper function

    Returns a dictionary containing data used for pagination
    """
    BOOKS_PER_PAGE = 8

    # Gets the number of pages for pagination
    number_of_pages = math.ceil(number_of_books / BOOKS_PER_PAGE)

    # For chevron links
    previous_page = int(page) - 1
    next_page = int(page) + 1

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


@app.route("/book/<book_id>", methods=["GET", "POST"])
def book(book_id):
    """
    Returns template for Book page

    Gets book information, including all reviews associated
    with the book
    """

    # "review_id_to_edit" and "old_review" values are set
    # when user clicks "Edit" button on a review.
    review_id_to_edit = request.args.get('review_id', None)
    old_review = mongo.db.reviews.find_one(
        {"_id": ObjectId(review_id_to_edit)}
    )

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    # https://stackoverflow.com/questions/51244068/pymongo-how-to-check-if-field-exists

    reviews = list(mongo.db.reviews.find(
        {
            "$query": {"book_id": {"$eq": book_id}},
            "$orderby": {"review_date": -1}
        })
    )

    # calculate review rating percentage
    no_of_reviews = len(reviews)
    rating_percentage = get_rating(reviews, no_of_reviews, book)

    return render_template(
        "book.html",
        book=book, reviews=reviews,
        no_of_reviews=no_of_reviews,
        rating=rating_percentage,
        review_id_to_edit=review_id_to_edit,
        old_review=old_review
    )


def get_rating(reviews, no_of_reviews, book):
    """
    Helper function

    1. Gets sum of all ratings for the book

    2. Updates rating value for the book in
    the books collection

    3. Calculates the rating percentage for a book
    Used for filling the stars display
    """

    # gets the sum of all the ratings for this book
    total_rating = 0
    for review in reviews:
        total_rating += review["rating"]

    # update total_rating value for this book
    book["total_rating"] = total_rating
    mongo.db.books.update({"_id": ObjectId(book["_id"])}, book)

    # gets rating percentage
    rating_percentage = 0

    if no_of_reviews > 0:
        rating_average = total_rating / no_of_reviews
        rating_percentage = (rating_average / 5.0) * 100

    return rating_percentage


@app.route("/add_review/<book_id>", methods=["GET", "POST"])
def add_review(book_id):
    """
    Adds a review to the reviews collection

    Redirects to the Book page on which the review was added
    """
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
        mongo.db.reviews.insert_one(review)
        flash("Review added!", "success")
        return redirect(url_for("book", book_id=book_id))


@app.route("/edit_review/<book_id>", methods=["GET", "POST"])
def edit_review(book_id):
    """
    Updates the specific review in the reviews collection

    Redirects to the Book page on which the review is located
    """
    review_id = request.args.get('review_id', None)
    old_review = mongo.db.reviews.find_one(
        {"_id": ObjectId(review_id)}
    )

    if request.method == "POST":
        # Edit Review
        edited_review = {
            "title": request.form.get("title"),
            "comment": request.form.get("comment"),
            "book_id": book_id,
            "reviewed_by": old_review["reviewed_by"],
            "review_date": old_review["review_date"],
            "rating": int(request.form.get("stars"))
        }

        mongo.db.reviews.update({"_id": ObjectId(review_id)}, edited_review)
        flash("Review edited!", "success")
        return redirect(url_for("book", book_id=book_id))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Returns template for Contact page

    Takes in form data and sends it as an email
    to the site administrator
    """

    if request.method == "POST":
        # gets contact form data
        name = request.form.get("name")
        email = request.form.get("email")
        comment = request.form.get("comment")

        # puts together message
        msg = Message(
                subject=f"Mail from {name}",
                body=f"Name: {name}\nE-Mail: {email}\n\n\n{comment}",
                sender=email,
                recipients=[os.environ.get("MAIL_USERNAME")]
        )

        # tries to send message
        exception_exists = False
        try:
            mail.send(msg)
        except SMTPException as e:
            exception_exists = True
            print(e)

        # flash message for whether or not email was sent
        if exception_exists:
            flash("Email could not be sent", "error")
        else:
            flash("Email sent!", "success")

    return render_template("contact.html", success=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Returns template for Register page

    Inserts user if username doesn't already exist
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists", "error")
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
        flash("Registration Successful!", "success")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Returns template for the Login page

    Once form data is submitted, checks if user exists.
    Also checks if password is correct.

    Redirects to Profile page if data is correct
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password", "error")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Removes user from session cookie

    Redirects to the Login page
    """
    session.pop("user")

    flash("You have been logged out", "success")

    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Returns template for Profile page is user is in session

    All books associated with the user will be displayed on
    this page
    """
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        # get all books associated with the user
        books = list(mongo.db.books.find({"uploaded_by": username}))

        return render_template("profile.html", username=username, books=books)

    return redirect(url_for("login"))


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Returns template for Add Book page

    Adds book to the books collection
    """
    if request.method == "POST":
        # Create book document for books collection
        book = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "genre": request.form.get("genre"),
            "image": request.form.get("image"),
            "description": request.form.get("description"),
            "uploaded_by": session["user"],
            "total_rating": 0
        }
        mongo.db.books.insert_one(book)
        flash("Book successfully added to the library!", "success")
        return redirect(url_for("get_books"))

    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("add-book.html", genres=genres)


@app.route("/edit_book/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    """
    Returns template for the Edit Book page

    Updates the details for the book in the books collection
    """
    if request.method == "POST":

        # gets some old book data that we don't want changed
        # i.e. book's rating (defined by reviewers) and who
        # the book was uploaded by
        old_book_data = mongo.db.books.find_one({"_id": ObjectId(book_id)})

        updated_book = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "genre": request.form.get("genre"),
            "image": request.form.get("image"),
            "description": request.form.get("description"),
            "uploaded_by": old_book_data["uploaded_by"],
            "rating": old_book_data["total_rating"]
        }
        mongo.db.books.update({"_id": ObjectId(book_id)}, updated_book)
        flash("Book Successfully Edited", "success")
        return redirect(url_for("book", book_id=book_id))

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("edit-book.html", book=book, genres=genres)


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    """
    Removes the book selected on the Book page from the database

    Also removes all reviews associated with the book

    Redirects to the Books page
    """
    mongo.db.books.remove({"_id": ObjectId(book_id)})

    # Delete all reviews associated with the book
    query = {"book_id": {"$eq": book_id}}
    mongo.db.reviews.remove(query)

    flash("Book Successfully Deleted", "success")
    return redirect(url_for("get_books"))


@app.route("/delete_review/<book_id>")
def delete_review(book_id):
    """
    Removes the review selected on the Book page from the database

    Redirects to the same Book page
    """
    review_id = request.args.get('review_id', None)

    mongo.db.reviews.remove({"_id": ObjectId(review_id)})

    flash("Review Successfully Deleted", "success")
    return redirect(url_for("book", book_id=book_id))


# tells app how and where to host application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
