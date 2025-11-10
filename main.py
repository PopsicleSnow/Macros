from math import inf, isinf
from flask import Flask, render_template, jsonify, request, redirect
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
    "localxdesign": "Local x Design",
    "ladleandleaf": "Ladle and Leaf",
    "undergroundpizza": "Underground Pizza",
    "monsoon": "Monsoon",
    "almaregelato": "Almare Gelato"
}

LOCATION_CATEGORIES = {
    "cafe3": "dining",
    "clarkkerr": "dining",
    "foothill": "dining",
    "crossroads": "dining",
    "gbc": "cafe",
    "browns": "cafe",
    "localxdesign": "cafe",
    "ladleandleaf": "studentunion",
    "undergroundpizza": "studentunion",
    "monsoon": "studentunion",
    "almaregelato": "studentunion"
}

def get_display_name(location_key):
    """Convert internal location key to display name"""
    return LOCATION_DISPLAY_NAMES.get(location_key, location_key)

def get_location_category(location_key):
    """Get category for a location"""
    return LOCATION_CATEGORIES.get(location_key, "other")

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
    
@app.before_request
def redirect_old_domain():
    """Redirect from macros.kuljitu.com to ucbmacros.com."""
    host = request.host.lower()
    if host == 'macros.kuljitu.com':
        # Create the new URL with the same path and query string
        new_url = request.url.replace(
            'macros.kuljitu.com', 
            'ucbmacros.com', 
            1
        )
        return redirect(new_url, code=301)

@app.route('/')
def index():
    locations = list_firebase_locations()
    return render_template('index.html', locations=list(locations),
                          get_display_name=get_display_name,
                          get_category=get_location_category)

@app.route('/<location>')
def location_page(location):
    """Dynamic route handler for all location pages"""
    # Validate that the location exists
    if location not in LOCATION_DISPLAY_NAMES:
        return "Location not found", 404

    return render_template('location.html',
                         name=LOCATION_DISPLAY_NAMES[location],
                         data_name=location)

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
    food_items = []  # Store individual food items for logging

    for name, values in food.items():
        if len(values) != 6:
            return "Error"
        values = [number_parser(j) for j in values]
        servings = values[0]

        # Calculate totals
        data["calories"] += values[1] * servings if values[1] > 0 and not isinf(values[1]) else 0
        data["fat"] += values[2] * servings if values[2] > 0 and not isinf(values[2]) else 0
        data["carbs"] += values[3] * servings if values[3] > 0 and not isinf(values[3]) else 0
        data["protein"] += values[4] * servings if values[4] > 0 and not isinf(values[4]) else 0
        data["sugar"] += values[5] * servings if values[5] > 0 and not isinf(values[5]) else 0

        # Store individual food item data for logging
        food_items.append({
            "name": f"{name} ({servings})",
            "calories": values[1] * servings if values[1] > 0 and not isinf(values[1]) else 0,
            "fat": values[2] * servings if values[2] > 0 and not isinf(values[2]) else 0,
            "carbs": values[3] * servings if values[3] > 0 and not isinf(values[3]) else 0,
            "protein": values[4] * servings if values[4] > 0 and not isinf(values[4]) else 0,
            "sugar": values[5] * servings if values[5] > 0 and not isinf(values[5]) else 0
        })

    return render_template('result.html', data=data, food_items=food_items)

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
    # App Engine cron requests come from IP 0.1.0.2 and have X-Appengine-Cron header
    is_cron = request.headers.get('X-Appengine-Cron') == 'true'

    if is_cron:
        upload_menu_to_firestore()
        return "Updated", 200

    return "Unauthorized", 403

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
