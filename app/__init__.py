import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# change password to parameter using .env variables
app.config[ "SQLALCHEMY_DATABASE_URI" ] = "postgresql://postgres:pass@localhost:5432/streeteatsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

friends = db.Table('friends',
    db.Column("user_id_fk", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
)
'''To override the table name, set the __tablename__ class attribute.'''
# creates user table
class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    friendship = db.relationship("UserModel",
                    secondary=friends,
                    primaryjoin=user_id==friends.c.user_id_fk,
                    secondaryjoin=user_id==friends.c.friend_id,
                    backref="followed_by"
    )
    # friendships = db.relationship('users', backref='user', lazy=True)
        
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

class ListModel(db.Model):
    __tablename__ = "lists"

    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listname = db.Column(db.String())
    user_id_fk = db.Column(db.String())

    def __init__(self, listname, user_id_fk):
        self.listname = listname
        self.user_id_fk = user_id_fk

    def __repr__(self):
        return f"<User {self.listname}>"


# class FriendModel(db.Model):
#     ___tablename___ = "friends"

#     user_id_fk = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

load_dotenv()
db.create_all()

@app.route("/")
def index():
    return render_template("index.html", title="StreetEats", url=os.getenv("URL"))

# create health end point
@app.route("/health")
def check():
    return "Working"

@app.route("/register", methods=("GET", "POST"))
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
            return f"User {username} created successfully"
        else:
            return error, 418

    return render_template("register.html", title="Register")
