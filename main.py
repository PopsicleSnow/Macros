from flask import Flask, render_template, jsonify, request
from query_database import query
from itertools import chain
import sqlite3

#####
"""Web App"""
# next:
# present option to choose mealperiods
# update_database.py and menu.py both run locations(), fix to only do once
# future:
# show location options, mealperiod options, in same page, one after another
# save foods to historical database
#####

app = Flask(__name__)

def dict_factory(cursor, row):
    return [value for value in row]

def query_db(statement):
    conn = sqlite3.connect("menu.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(statement)
    data = cursor.fetchall()
    conn.close()
    data = list(chain.from_iterable(data))
    return data

@app.route('/')
def index():
    locations = query_db("SELECT name FROM sqlite_master")
    return render_template('index.html', locations=list(locations))

@app.route('/Cafe3')
def cafe3():
    if "Cafe3" in query_db("SELECT name FROM sqlite_master"):
        return render_template('cafe3.html')
    return render_template('closed.html')

@app.route('/Crossroads')
def crossroads():
    if "Crossroads" in query_db("SELECT name FROM sqlite_master"):
        return render_template('crossroads.html')
    return render_template('closed.html')

@app.route('/Foothill')
def foothill():
    if request.get_data():
        return request.get_data()
    if "Foothill" in query_db("SELECT name FROM sqlite_master"):
        return render_template('foothill.html')
    return render_template('closed.html')

@app.route('/ClarkKerr')
def clarkkerr():
    if "ClarkKerr" in query_db("SELECT name FROM sqlite_master"):
        return render_template('clarkkerr.html')
    return render_template('closed.html')

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
        data["calories"] += i[1] * i[0] if i[1] > 0 else 0
        data["fat"] += i[2] * i[0] if i[2] > 0 else 0
        data["carbs"] += i[3] * i[0] if i[3] > 0 else 0
        data["protein"] += i[4] * i[0] if i[4] > 0 else 0
        data["sugar"] += i[5] * i[0] if i[5] > 0 else 0
    return render_template('result.html', data=data)

@app.route('/get_data')
def get_data():
    mealperiod = request.args.get('mealperiod')
    location = request.args.get('location')
    # Logic to fetch data from the database based on the category
    if mealperiod and location and location in query_db("SELECT name FROM sqlite_master"):
        try:
            data = query(mealperiod, location)
            return jsonify(data)
        except:
            return "Error"
    return "Error"

@app.route('/mealperiods')
def mealperiods():
    location = request.args.get('location')
    if location in query_db("SELECT name FROM sqlite_master"):
        try:
            data = query_db(f"SELECT DISTINCT mealperiod FROM {location}")
            return jsonify(data)
        except:
            return "Error"
    return "Error"

if __name__ == '__main__':
    app.run(debug=True)
