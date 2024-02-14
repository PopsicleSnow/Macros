from google.cloud import firestore

def query(mealperiod, location):
    # Initialize Firestore client
    db = firestore.Client()

    # Reference to the collection
    collection_ref = db.collection(location)

    # Query Firestore for documents matching mealperiod
    query = collection_ref.where(field_path="mealperiod", op_string="==", value=mealperiod).get()

    # Extract data from documents
    return [doc.to_dict() for doc in query]

# Example usage:
# print(query("Breakfast - Spring", "Foothill"))
