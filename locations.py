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
    locations["Cafe3"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Cafe_3_{today}.xml")
    locations["ClarkKerr"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Clark_Kerr_Campus_{today}.xml")
    locations["Foothill"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Foothill_{today}.xml")
    locations["Crossroads"] = requests.get(f"https://dining.berkeley.edu/wp-content/uploads/xml_files/Crossroads_{today}.xml")
    for location in tuple(locations):
        if locations[location].status_code != 200:
            locations.pop(location)
    return locations