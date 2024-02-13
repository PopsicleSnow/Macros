from locations import locations
from lxml import etree as ET

def menu(loc):
    # Get xml from web request
    loc = locations()[loc]
    root = ET.fromstring(loc.text)

    # Create dictionary for each dish
    data = {}
    nutrient_list = None
    for mealperiod in root:
        mealperiod_name = mealperiod.get("mealperiodname")
        nutrients_element = mealperiod.find("nutrients")
        data[mealperiod_name] = {}
        if nutrients_element is not None:
            nutrient_list = nutrient_list or nutrients_element.text.split('|')[:-1]
            for recipes in mealperiod.findall('recipes'):
                for recipe in recipes.findall('recipe'):
                    recipe_data = data[mealperiod_name][recipe.get("shortName")] = {}
                    recipe_data["category"] = recipe.get("category")
                    recipe_data["servingSize"] = recipe.get("servingSize") + recipe.get("servingSizeUnit")
                    nutrient_data = recipe.get("nutrients").split('|')[:-1]
                    for nutrient in nutrient_list:
                        recipe_data[nutrient] = str(max(0, float(nutrient_data[nutrient_list.index(nutrient)])))
    return data
