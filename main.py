from flask import Flask, render_template
from locations import locations

#####
"""Web App"""
#####

locations = locations()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', locations=list(locations.keys()))

@app.route('/Cafe3')
def cafe3():
    if "Cafe3" in locations.keys():
        return render_template('cafe3.html')
    return render_template('closed.html')

@app.route('/Crossroads')
def crossroads():
    if "Crossroads" in locations.keys():
        return render_template('crossroads.html')
    return render_template('closed.html')

@app.route('/Foothill')
def foothill():
    if "Foothill" in locations.keys():
        return render_template('foothill.html')
    return render_template('closed.html')

@app.route('/ClarkKerr')
def clarkkerr():
    if "ClarkKerr" in locations.keys():
        return render_template('clarkkerr.html')
    return render_template('closed.html')

if __name__ == '__main__':
    app.run(debug=True)
