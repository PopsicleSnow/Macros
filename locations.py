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
        Dict of <Request objects>
    """
    locations = {}
    today = datetime.now(pytz.timezone('America/Los_Angeles') ).strftime("%Y%m%d")
    locations["cafe3"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Cafe_3_{today}.xml")
    locations["clarkkerr"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Clark_Kerr_Campus_{today}.xml")
    locations["foothill"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Foothill_{today}.xml")
    locations["crossroads"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Crossroads_{today}.xml")
    locations["gbc"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Golden_Bear_Cafe_{today}.xml")
    locations["localxdesign"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/menus-exportimport/Local_x_Design_{today}.xml")
    for location in tuple(locations):
        if locations[location].status_code != 200:
            locations.pop(location)
    return locations