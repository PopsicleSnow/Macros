import requests
from datetime import datetime
import pytz

#####
"""Get the menu items from the database"""
"""TODO:Move locations to update_database.py
        Query database and format data.
        Create function that queries menu page to see what locations are open"""
#####

def locations():
    """
    Finds open dining halls at UC Berkeley.

    Returns:
        Dict where keys are location identifiers and values are either:
        - Request objects for single-location venues
        - Tuples of (Request object, category_filter) for multi-location venues
    """
    locations = {}
    today = datetime.now(pytz.timezone('America/Los_Angeles') ).strftime("%Y%m%d")

    # Single-location venues
    locations["cafe3"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Cafe_3_{today}.xml")
    locations["clarkkerr"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Clark_Kerr_Campus_{today}.xml")
    locations["foothill"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Foothill_{today}.xml")
    locations["crossroads"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Crossroads_{today}.xml")
    locations["gbc"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Golden_Bear_Cafe_{today}.xml")
    locations["localxdesign"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Local_x_Design_{today}.xml")
    locations["browns"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Browns_Cafe_{today}.xml")

    # Multi-location venue: Student Union Eateries
    # These all share the same XML file but are filtered by category
    student_union_request = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Eateries_at_the_Student_Union_{today}.xml")
    if student_union_request.status_code == 200:
        locations["ladleandleaf"] = (student_union_request, "Ladle and Leaf")
        locations["undergroundpizza"] = (student_union_request, "Underground Pizza")
        locations["monsoon"] = (student_union_request, "Monsoon")
        locations["almaregelato"] = (student_union_request, "Almare Gelato")

    # Remove failed requests for single-location venues
    for location in tuple(locations):
        value = locations[location]
        # Check if it's a single request or a tuple
        if isinstance(value, tuple):
            # It's a multi-location entry, already validated above
            continue
        elif value.status_code != 200:
            locations.pop(location)

    return locations