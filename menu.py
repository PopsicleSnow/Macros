from lxml import etree as ET

def menu(locations_request, category_filter=None):
    """
    Parse menu XML and return dish data.

    Args:
        locations_request: HTTP response object containing XML data
        category_filter: Optional string to filter recipes by category prefix
                        (e.g., "Ladle and Leaf" will match "Ladle and Leaf - Soup")

    Returns:
        Dictionary of meal periods with dish data
    """
    # Get xml from web request
    loc = locations_request
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
                    recipe_category = recipe.get("category")

                    # Skip this recipe if it doesn't match the category filter
                    if category_filter and not recipe_category.startswith(category_filter):
                        continue

                    recipe_data = data[mealperiod_name][recipe.get("shortName")] = {}
                    recipe_data["category"] = recipe_category
                    recipe_data["servingSize"] = recipe.get("servingSize") + recipe.get("servingSizeUnit")
                    nutrient_data = recipe.get("nutrients").split('|')[:-1]
                    for nutrient in nutrient_list:
                        recipe_data[nutrient] = str(max(0, float(nutrient_data[nutrient_list.index(nutrient)])))
    return data
