import os
from flask import Flask
if os.path.exists("env.py"):
    import env


# Creates instance of Flask
app = Flask(__name__)

# Default root
@app.route("/")
def hello():
    return "Hello World!"


# Tells app how and where to host application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)