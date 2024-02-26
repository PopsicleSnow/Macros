from google.cloud import firestore
from locations import locations
from menu import menu

def upload_menu_to_firestore():
    # Initialize Firestore client
    db = firestore.Client()

    # delete locations collection items
    location_collection = db.collection("locations")
    location_docs = location_collection.stream()
    for doc in location_docs:
        doc.reference.delete()
    location_list = []

    locations_requests = locations()
    for loc in locations_requests:
        curr_mealperiods = []
        dishes = menu(locations_requests[loc])
        location_list.append(loc)

        # Reference to the collection
        collection_ref = db.collection(loc)

        # Delete existing documents in the collection
        docs = collection_ref.stream()
        for doc in docs:
            doc.reference.delete()

        # Prepare data for bulk insert
        data_to_insert = []
        for mealperiod in dishes:
            for dish in dishes[mealperiod]:
                dish_data = dishes[mealperiod][dish]
                data_to_insert.append({
                    "mealperiod": mealperiod,
                    "category": dish_data["category"],
                    "name": dish.strip(),
                    "calories": dish_data["Calories (kcal)"],
                    "fat": dish_data["Total Lipid/Fat (g)"],
                    "carbs": dish_data["Carbohydrate (g)"],
                    "protein": dish_data["Protein (g)"],
                    "sugar": dish_data["Sugar (g)"],
                    "servingSize": dish_data["servingSize"]
                })
            curr_mealperiods.append(mealperiod)

        # Batch upload data to Firestore
        batch = db.batch()
        for data in data_to_insert:
            doc_ref = collection_ref.document()
            batch.set(doc_ref, data)
        batch.set(collection_ref.document("mealperiods"), {"periods": curr_mealperiods})
        batch.commit()
    location_collection.document().set({"names": location_list + ["GBC"]})