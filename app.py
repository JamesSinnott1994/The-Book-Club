import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


# Creates instance of Flask
app = Flask(__name__)

# App configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("URI")
app.secret_key = os.environ.get("SECRET_KEY") # Required for some Flask functions

# Instance of PyMongo
# Ensures our Flask app is properly communicating with the Mongo database
mongo = PyMongo(app)

# Default root
@app.route("/")
def hello():
    return "Hello World!"


# Tells app how and where to host application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)