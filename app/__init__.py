import os
from flask import Flask, render_template, request, g
from dotenv import load_dotenv
import requests
from flask import request
from . import api
from app.api import api_run1
from app.api import apiYelp
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

lat, long = api_run1()
ENDPOINT_YELP, HEADERS_YELP = apiYelp()

app.config[ "SQLALCHEMY_DATABASE_URI" ] = "postgresql://postgres:pass@localhost:5432/streeteatsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class user_category:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def repr(self):
        return self.type


# class Restaurant:
#     def __init__(self, name, businessID):
#         self.name = name
#         self.businessID = businessID


# restaurants
@app.route("/", methods=["GET", "POST"])
def index():
    testLocation = "toronto"
    category = ""
    city = None

    if request.method == "POST":
        city = request.form.get("city")
        selection = request.form.get("type")
        S = user_category(selection, testLocation)
        category = S.repr()

    if city:
        PARAMETERS_YELP = {
            "term": category,
            "limit": 50,
            "offset": 50,
            "radius": 10000,
            "location": city,
        }
    else:
        PARAMETERS_YELP = {
            "term": category,
            "limit": 50,
            "offset": 50,
            "radius": 10000,
            "latitude": lat,
            "longitude": long,
        }

#check if it is already in the database
# if it is in , return it from db
# if not, add to database and return to user 

    response = requests.get(
        url=ENDPOINT_YELP, params=PARAMETERS_YELP, headers=HEADERS_YELP
    )
    business_data = response.json()

    # choose list
    # is business id already in db-list?
    # if it is, do nothing
    # if not, add to database 

    # print(business_data)

    return render_template(
        "index.html",
        title="StreetEats",
        url=os.getenv("URL"),
        data=business_data,
    )
    # return render_template("index.html", title="StreetEats", url=os.getenv("URL"))

# create health end point
@app.route("/health")
def check():
    return "Working"

@app.route("/userpage")
def userpage():
    return render_template(
        "userpage.html", title="My Account", url=os.getenv("URL")
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        from .db import UserModel, db

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
    from .db import UserModel
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
            #Return home page upon successful registration, assuming it's "index.html"
            return index()
        else:
            return error, 418

    # Return a login page
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)