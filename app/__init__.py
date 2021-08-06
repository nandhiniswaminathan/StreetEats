import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from flask import request


load_dotenv()
app = Flask(__name__)

# API #1
ENDPOINT_IP = "https://api.ipify.org?format=json"  # method: GET
response_ip = requests.get(url=ENDPOINT_IP)
ip = response_ip.json()["ip"]
# print(ip)

# API #2
ENDPOINT_LOC = f"https://ipinfo.io/{ip}?token=e5705a55652e77"  # method: GET
response_loc = requests.get(url=ENDPOINT_LOC)
# print(response_loc)

response_new = response_loc.json()["loc"].split(",")
lat, long = response_new[0], response_new[1]


client_id = "_yVwgo9pbZN4s883GVMXyg"
API_KEY_YELP = os.getenv('APIKEYYELP')
ENDPOINT_YELP = "https://api.yelp.com/v3/businesses/search"  # method: GET
HEADERS_YELP = {"Authorization": "bearer %s" % API_KEY_YELP}


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
