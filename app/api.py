import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from flask import request


def api_run1():

    # API #1
    ENDPOINT_IP = "https://api.ipify.org?format=json"  # method: GET
    response_ip = requests.get(url=ENDPOINT_IP)
    ip = response_ip.json()["ip"]
    print(ip)

    # API #2
    ENDPOINT_LOC = f"https://ipinfo.io/{ip}?token=e5705a55652e77"  # method: GET
    response_loc = requests.get(url=ENDPOINT_LOC)
    print(response_loc)

    response_new = response_loc.json()["loc"].split(",")
    lat, long = response_new[0], response_new[1]

    return lat, long


def apiYelp():
    client_id = "_yVwgo9pbZN4s883GVMXyg"
    API_KEY_YELP = os.getenv("APIKEYYELP")
    ENDPOINT_YELP = "https://api.yelp.com/v3/businesses/search"  # method: GET
    HEADERS_YELP = {"Authorization": "bearer %s" % API_KEY_YELP}

    return ENDPOINT_YELP, HEADERS_YELP
