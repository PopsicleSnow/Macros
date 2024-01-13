from locations import locations
import xml.etree.ElementTree as ET

def menu(loc):
    # Get xml from web request
    loc = locations()[loc]
    root = ET.fromstring(loc.text)

    # Create dictionary for each dish
    data = {}
    nutrient_list = None
    for mealperiod in root:
        mealperiod_name = mealperiod.attrib["mealperiodname"]
        nutrients_element = mealperiod.find("nutrients")
        data[mealperiod_name] = {}
        if nutrients_element is not None:
            nutrient_list = nutrient_list or nutrients_element.text.split('|')[:-1]
            for recipes in mealperiod.findall('recipes'):
                for recipe in recipes.findall('recipe'):
                    recipe_data = data[mealperiod_name][recipe.attrib["shortName"]] = {}
                    recipe_data["category"] = recipe.attrib["category"]
                    recipe_data["servingSize"] = recipe.attrib["servingSize"] + recipe.attrib["servingSizeUnit"]
                    nutrient_data = recipe.attrib["nutrients"].split('|')[:-1]
                    for nutrient in nutrient_list:
                        recipe_data[nutrient] = nutrient_data[nutrient_list.index(nutrient)]
    return data
