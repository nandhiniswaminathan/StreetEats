import os
import json
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session


load_dotenv()
app = Flask(__name__)
<<<<<<< HEAD
app.config[ "SQLALCHEMY_DATABASE_URI" ] = "postgresql://postgres:pass@localhost:5432/streeteatsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# create user table
class UserModel(db.Model):
    __tablename__ = "users"
    #Add user id, username, password columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    #todo add column for restaurant lists, friend list

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

class BusinessList(db.Model):
    __tablename__ = "BusinessLists"
    #Add id of list, name of list, business_id columns
    list_name = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer)
    #todo add column for restaurant lists, friend list

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"
=======
api_key = ""
API_HOST = "https://www.yelp.com/developers/documentation/v3/business_search"
headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
>>>>>>> 7c9a7efe43414915ed16c6d616280898573dccba

load_dotenv()
db.create_all()


@app.route("/")
def index():
    return render_template("index.html", title="StreetEats", url=os.getenv("URL"))


# create health end point
@app.route("/health")
def check():
    return "Working"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            #Return login page upon successful registration
            return render_template("login.html")
        else:
            return error, 418

    # Return a register page
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            #Return home page upon successful registration, assuming it's "home.html"
            return render_template("index.html")
        else:
            return error, 418

    # Return a login page
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
