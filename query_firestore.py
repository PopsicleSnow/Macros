from google.cloud import firestore

def query(mealperiod, location):
    # Initialize Firestore client
    db = firestore.Client()

    # Reference to the collection
    collection_ref = db.collection(location)

    # Query Firestore for documents matching mealperiod
    query = collection_ref.where("mealperiod", "==", mealperiod).get()

    # Extract data from documents
    result = []
    for doc in query:
        data = doc.to_dict()
        result.append(data)

    return result

# Example usage:
# print(query("Breakfast - Spring", "Foothill"))
