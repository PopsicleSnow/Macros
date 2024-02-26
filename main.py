from math import inf
from flask import Flask, render_template, jsonify, request
from query_firestore import query
from update_firestore import upload_menu_to_firestore
from locations import locations
from google.cloud import firestore

#####
"""Web App"""
# present option to choose mealperiods
# update_database.py and menu.py both run locations(), fix to only do once
# future:
# show location options, mealperiod options, in same page, one after another
# save foods to historical database
#####

app = Flask(__name__)

def list_locations():
    return locations()

def list_firebase_locations():
    db = firestore.Client()
    locations = db.collection("locations").limit(1).get()[0].to_dict().get("names", [])
    return locations

def list_mealperiods(location):
    db = firestore.Client()
    mealperiods = db.collection(location).document("mealperiods").get().to_dict().get("periods", [])
    return mealperiods
    
@app.route('/')
def index():
    locations = list_firebase_locations()
    return render_template('index.html', locations=list(locations))

@app.route('/Cafe3')
def cafe3():
    return render_template('location.html', name="Cafe 3", data_name="Cafe3")

@app.route('/Crossroads')
def crossroads():
    return render_template('location.html', name="Crossroads", data_name="Crossroads")

@app.route('/Foothill')
def foothill():
    return render_template('location.html', name="Foothill", data_name="Foothill")

@app.route('/ClarkKerr')
def clarkkerr():
    return render_template('location.html', name="Clark Kerr", data_name="ClarkKerr")

@app.route('/GBC')
def gbc():
    return render_template('location.html', name="GBC", data_name="GBC")

@app.route('/result')
def result():
    if not request.args:
        return "Error"
    food = {item: request.args.getlist(item) for item in request.args if request.args.get(item) != ""}
    # make sure all values are integers
    try:
        food = {item: [float(i) for i in food[item]] for item in food}
    except:
        return "Error"
    # add up all the values
    data = {"calories": 0, "fat": 0, "carbs": 0, "protein": 0, "sugar": 0}
    for i in food.values():
        if len(i) != 6:
            return "Error"
        data["calories"] += i[1] * i[0] if i[1] > 0 and i[1] != inf else 0
        data["fat"] += i[2] * i[0] if i[2] > 0 and i[2] != inf else 0
        data["carbs"] += i[3] * i[0] if i[3] > 0 and i[3] != inf else 0
        data["protein"] += i[4] * i[0] if i[4] > 0 and i[4] != inf else 0
        data["sugar"] += i[5] * i[0] if i[5] > 0 and i[5] != inf else 0
    return render_template('result.html', data=data)

@app.route('/get_data')
def get_data():
    mealperiod = request.args.get('mealperiod')
    location = request.args.get('location')
    # Logic to fetch data from the database based on the category
    if mealperiod and location and location in list_firebase_locations():
        try:
            data = query(mealperiod, location)
            return jsonify(data)
        except:
            return "Error"
    return "Mealperiod and/or location doesn't exist or is not provided"

@app.route('/mealperiods')
def mealperiods():
    location = request.args.get('location')
    if location and location in list_firebase_locations():
        try:
            return jsonify(list_mealperiods(location))
        except:
            return "Error"
    return "Location doesn't exist or not provided"

@app.route('/tasks/update')
def update():
    if request.headers['X-Appengine-Cron'] == "true":
        upload_menu_to_firestore()
        return "Updated"
    return "Error"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
