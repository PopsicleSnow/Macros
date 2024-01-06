import requests
from bs4 import BeautifulSoup

#####
"""Get the menu items"""
#####

response = requests.get("https://dining.berkeley.edu/menus/")

soup = BeautifulSoup(response.text, 'html.parser')

foothill = soup.find_all("li", class_="Foothill")[0]
meals = foothill.find_all("li", class_="preiod-name")

food_options = {}
for meal in meals:
    meal_name = next(meal.span.strings)
    food_options[meal_name] = {}
    for typemeal in meal.find_all("div", class_="cat-name"):
        food_options[meal_name][typemeal.span.string] = []
        for item in typemeal.find_all("li"):
            food_options[meal_name][typemeal.span.string] += [{"name": item.span.string, "id":item['data-id'], "menuid":item['data-menuid']}]
print(food_options)

####
"""Get nutritional facts"""
####

location = ""
id = ""

d = {'action':'get_recipe_details', 'location':location, 'id':id}
response = requests.post("https://dining.berkeley.edu/wp-admin/admin-ajax.php", data=d)

print(response.text)

##### Below is the flask code #####
## Fix the food_options stuff

from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        id = request.form['id']
        d = {'action': 'get_recipe_details', 'location': location, 'id': id}
        response = requests.post("https://dining.berkeley.edu/wp-admin/admin-ajax.php", data=d)
        return response.text
    else:
        options = ''
        for meal, types in food_options.items():
            options += f'<h3>{meal}</h3>'
            for typemeal, items in types.items():
                options += f'<h4>{typemeal}</h4>'
                for item in items:
                    options += f'<p>{item["name"]}</p>'
                    options += f'<form method="POST" action="/">'
                    options += f'<input type="hidden" name="location" value="{item["menuid"]}">'
                    options += f'<input type="hidden" name="id" value="{item["id"]}">'
                    options += f'<button type="submit">Select</button>'
                    options += f'</form>'
        return options

if __name__ == '__main__':
    app.run(debug=True)
