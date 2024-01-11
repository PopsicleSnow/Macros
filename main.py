import requests
from datetime import datetime
import pytz
from flask import Flask, render_template

#####
"""Get the menu items"""
"""TODO:Use react for dining halls 
        Add to database"""
#####

locations = {}
today = datetime.now(pytz.timezone('America/Los_Angeles') ).strftime("%Y%m%d")
locations["Cafe3"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Cafe_3_{today}.xml")
locations["ClarkKerr"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Clark_Kerr_{today}.xml")
locations["Foothill"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Foothill_{today}.xml")
locations["Crossroads"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Crossroads_{today}.xml")

for location in tuple(locations):
    if locations[location].status_code != 200:
        locations.pop(location)

#####
"""Web App"""
#####

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', locations=list(locations.keys()))

@app.route('/Cafe3')
def cafe3():
    if "Cafe3" in locations:
        return render_template('cafe3.html')
    return render_template('closed.html')

@app.route('/Crossroads')
def crossroads():
    if "Crossroads" in locations:
        return render_template('crossroads.html')
    return render_template('closed.html')

@app.route('/Foothill')
def foothill():
    if "Foothill" in locations:
        return render_template('foothill.html')
    return render_template('closed.html')

@app.route('/ClarkKerr')
def clarkkerr():
    if "ClarkKerr" in locations:
        return render_template('clarkkerr.html')
    return render_template('closed.html')

if __name__ == '__main__':
    app.run(debug=True)
