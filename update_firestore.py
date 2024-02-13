from google.cloud import firestore
from locations import locations
from menu import menu

def upload_menu_to_firestore():
    # Initialize Firestore client
    db = firestore.Client()

    for loc in locations():
        dishes = menu(loc)

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

        # Batch upload data to Firestore
        batch = db.batch()
        for data in data_to_insert:
            doc_ref = collection_ref.document()
            batch.set(doc_ref, data)
        batch.commit()

# Execute the function to upload menu data to Firestore
upload_menu_to_firestore()
