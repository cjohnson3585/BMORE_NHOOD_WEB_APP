"""
Main app script that calls everything
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, subprocess
import qrcode
from PIL import Image
import subprocess
from functools import reduce
import sys
from shapely.geometry import Point
from check_nhood import check_nhood as cnd
from geopy.geocoders import Nominatim
import sys
import pandas as pd

application = Flask(__name__)


@application.route("/")
def welcome():
    return render_template("input.html")

@application.route("/receiver", methods=['POST', 'GET'])
def receiver():
    if request.method=='POST':
        default_name = '0'
        fn = request.form.get('fn', default_name)
        print(get_lat_long(fn))
        ott = get_lat_long(fn)
        return ('{},{},{},{},{}'.format(ott[0], ott[1], ott[2], ott[3],ott[4]))



def get_lat_long(address):
    try:
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.geocode(address)
        points = [Point(location.longitude, location.latitude)]
        for point in points:
            if str(cnd(point)[0]) != 'nan':
                return address, str(cnd(point)[0]), str(cnd(point)[1]), str(location.latitude), str(location.longitude)
            else:
                return address, 'nan', 'nan', str(location.latitude), str(location.longitude)
    except: 
        return address,'nan', 'nan', str(location.latitude), str(location.longitude)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
