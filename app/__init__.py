import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="StreetEats", url=os.getenv("URL"))


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
            return render_template("home.html")
        else:
            return error, 418

    # Return a login page
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
