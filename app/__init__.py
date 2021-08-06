import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from flask import request
from . import api
from app.api import api_run1
from app.api import apiYelp


load_dotenv()
app = Flask(__name__)

lat, long = api_run1()
ENDPOINT_YELP, HEADERS_YELP = apiYelp()


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

    response = requests.get(
        url=ENDPOINT_YELP, params=PARAMETERS_YELP, headers=HEADERS_YELP
    )
    business_data = response.json()
    # print(business_data)

    return render_template(
        "index.html",
        title="StreetEats",
        url=os.getenv("URL"),
        data=business_data,
    )
