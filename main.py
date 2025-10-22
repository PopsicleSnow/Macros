from math import inf, isinf
from flask import Flask, render_template, jsonify, request
from query_firestore import query
from update_firestore import upload_menu_to_firestore
from locations import locations
from google.cloud import firestore

#####
"""Web App"""
# group foods by category
# save foods to historical database
#####

app = Flask(__name__)

LOCATION_DISPLAY_NAMES = {
    "cafe3": "Cafe 3",
    "clarkkerr": "Clark Kerr",
    "foothill": "Foothill",
    "crossroads": "Crossroads",
    "gbc": "GBC",
    "browns": "Browns",
    "localxdesign": "Local x Design"
}

def get_display_name(location_key):
    """Convert internal location key to display name"""
    return LOCATION_DISPLAY_NAMES.get(location_key, location_key)

def list_locations():
    return locations()

def list_firebase_locations():
    db = firestore.Client()
    locations = db.collection("locations").document("locations").get().to_dict().get("names", [])
    return locations

def list_mealperiods(location):
    db = firestore.Client()
    mealperiods = db.collection(location).document("mealperiods").get().to_dict().get("periods", [])
    return mealperiods
    
def number_parser(value): 
    try:
        roundtest = round(value)
        inttest = int(value)
        if value < 0.1:
            return 0
        return value
    except:
        return 0

@app.route('/')
def index():
    locations = list_firebase_locations()
    return render_template('index.html', locations=list(locations),
                          get_display_name=get_display_name)

@app.route('/cafe3')
def cafe3():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["cafe3"], data_name="cafe3")

@app.route('/crossroads')
def crossroads():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["crossroads"], data_name="crossroads")

@app.route('/foothill')
def foothill():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["foothill"], data_name="foothill")

@app.route('/clarkkerr')
def clarkkerr():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["clarkkerr"], data_name="clarkkerr")

@app.route('/gbc')
def gbc():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["gbc"], data_name="gbc")

@app.route('/localxdesign')
def localxdesign():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["localxdesign"], data_name="localxdesign")

@app.route('/browns')
def browns():
    return render_template('location.html', name=LOCATION_DISPLAY_NAMES["browns"], data_name="browns")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST'])
def result():
    if not request.form:
        return "Error"
    food = {item: request.form.getlist(item) for item in request.form if request.form.get(item) != ""}
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
        i = [number_parser(j) for j in i]
        data["calories"] += i[1] * i[0] if i[1] > 0 and not isinf(i[1]) else 0
        data["fat"] += i[2] * i[0] if i[2] > 0 and not isinf(i[2]) else 0
        data["carbs"] += i[3] * i[0] if i[3] > 0 and not isinf(i[3]) else 0
        data["protein"] += i[4] * i[0] if i[4] > 0 and not isinf(i[4]) else 0
        data["sugar"] += i[5] * i[0] if i[5] > 0 and not isinf(i[5]) else 0
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
