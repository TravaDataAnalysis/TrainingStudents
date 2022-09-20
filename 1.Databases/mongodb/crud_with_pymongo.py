from training_db import TrainingMongoDB

if __name__ == '__main__':
    training_db = TrainingMongoDB()

    # Create operations
    doc = {
        "address": "So 1 Dai Co Viet",
        "borough": "Hai Ba Trung",
        "cuisine": "Lau nuong",
        "grades": "One Star",
        "name": "Lau nuong Bach Khoa",
        "restaurant_id": "00000001"
    }
    # Insert one document
    training_db.insert_one_restaurant(doc)
    docs = [
        {"address": "So 2 Dai Co Viet", "borough": "Hai Ba Trung", "restaurant_id": "00000002"},
        {"address": "So 3 Dai Co Viet", "borough": "Hai Ba Trung", "restaurant_id": "00000003"},
        {"address": "So 4 Dai Co Viet", "borough": "Hai Ba Trung", "restaurant_id": "00000004"}
    ]
    # Insert many documents
    training_db.insert_many_restaurants(docs)

    # Read operations
    # Get all documents in restaurants collection.
    all_restaurants = training_db.get_all_restaurants()
    print("There are all restaurants:")
    for restaurant in all_restaurants:
        print(restaurant)
    # Get a restaurant has id 00000004
    query = {"restaurant_id": "00000004"}
    a_restaurant = training_db.get_one_restaurant(query)
    print("\nThis is restaurant 00000004:", a_restaurant)

    # Update operations
    # Update one document
    training_db.update_one_restaurant()
    # Update many documents
    training_db.update_many_restaurants()

    # Delete operations
    # Delete one document has id 00000001
    training_db.delete_one_restaurant("00000001")
    # Delete many documents have id in restaurent_ids
    restaurant_ids = ["00000001", "00000002", "00000003", "00000004"]
    training_db.delete_many_restaurants(restaurant_ids)
