import os
import json
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)
app.config[ "SQLALCHEMY_DATABASE_URI" ] = "postgresql://postgres:pass@localhost:5432/streeteatsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

friends = db.Table('friends',
    db.Column("user_id_fk", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
)


# create user table
class UserModel(db.Model):
    __tablename__ = "users"
    #Add user id, username, password columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    lists = db.relationship("Lists", backref="List_OwnerID")
    #User has lists that refers to Lists db
    friendship = db.relationship("UserModel",
                    secondary=friends,
                    primaryjoin=user_id==friends.c.user_id_fk,
                    secondaryjoin=user_id==friends.c.friend_id,
                    backref="followed_by"
    )

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

class Lists(db.Model):
    __tablename__ = "lists"
    #Add id number of user who owns list, name of list, list_id number columns
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    businesses = db.relationship("BusinessList", backref="Business_ListID")
    #List db has businesses that refers to BusinessList/businesses db

### Need Help with where / how to connect and assign attributes for each user here
    def __init__(self, list_id, list_name, user_id):
        self.list_id = list_id
        self.list_name = list_name
        #self.user_id = user_id

    #def __repr__(self):
    #    return f"User {username} has list {}." # confused here
    #    self.business_id = #RETRIEVE from api
    #    self.business_name = #Restrieve id from api then retrieve name
    #    self.list_id = #Retrieve from lists db

class BusinessList(db.Model):
    __tablename__ = "businesses"
    #Add id number of list, name of business, business_id columns
    business_id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String())
    list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"))

### Need Help with where / how to connect and assign attributes for each business here
    def __init__(self, business_id, business_name, list_id):
        self.business_id = business_id
        self.business_name = business_name
        #self.list_id = list_id

    #def __repr__(self):
    #    return f"User {username} has list {}." # confused here
    #    self.business_id = #RETRIEVE from api
    #    self.business_name = #Restrieve id from api then retrieve name
    #    self.list_id = #Retrieve from lists db

db.create_all()


# class FriendModel(db.Model):
#     ___tablename___ = "friends"

#     user_id_fk = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

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
            #Return home page upon successful registration, assuming it's "index.html"
            return render_template("index.html")
        else:
            return error, 418

    # Return a login page
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
