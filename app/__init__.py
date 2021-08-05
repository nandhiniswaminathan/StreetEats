import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from apiKey import api_Key
from flask import request


load_dotenv()
app = Flask(__name__)

client_id = "_yVwgo9pbZN4s883GVMXyg"
API_KEY = api_Key
ENDPOINT = "https://api.yelp.com/v3/businesses/search"  # method: GET
HEADERS = {"Authorization": "bearer %s" % API_KEY}


class user_category:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def repr(self):
        return self.type


@app.route("/", methods=["GET", "POST"])
def index():
    testLocation = "toronto"

    if request.method == "POST":
        selection = request.form.get("type")
        S = user_category(selection, testLocation)
    category = S.repr()

    PARAMETERS = {
        "term": category,
        "limit": 50,
        "offset": 50,
        "radius": 10000,
        "location": testLocation,  # MUST CHANGE TO COORDINATES
    }

    response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    business_data = response.json()

    ENDPOINT_R = "https://api.yelp.com/v3/businesses/{id}/reviews"  # this doesnt work
    response_R = requests.get(url=ENDPOINT_R, headers=HEADERS)
    business_review = response_R.json()

    return render_template(
        "index.html",
        title="StreetEats",
        url=os.getenv("URL"),
        data=business_data,
        review=business_review,
    )
