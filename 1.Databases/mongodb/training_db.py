import logging
import sys

import pymongo
from pymongo.errors import ServerSelectionTimeoutError

from configs import MongoDBConfig
from constants import CollectionConstants
from constants import DbConstant

_LOGGER = logging.getLogger("MongoDB")


class TrainingMongoDB:
    def __init__(self, url=None):
        if url is None:
            url = MongoDBConfig.CONNECTION_URL
        try:
            self.client = pymongo.MongoClient(url)
            _LOGGER.info(f"Connected to MongoDB server on {url}")
        except ServerSelectionTimeoutError as e:
            _LOGGER.error(e)
            sys.exit(1)

        self.training_db = self.client[DbConstant.training_db]
        self.restaurants_col = self.training_db[CollectionConstants.restaurants_col]

    # Create
    def insert_one_restaurant(self, doc):
        self.restaurants_col.insert_one(doc)

    def insert_many_restaurants(self, docs):
        self.restaurants_col.insert_many(docs)

    # Read
    def get_all_restaurants(self):
        return self.restaurants_col.find({})

    def get_one_restaurant(self, query):
        return self.restaurants_col.find_one(query)

    # Update
    def update_one_restaurant(self):
        _filter = {"restaurant_id": "00000001"}
        update_operation = {"$set": {"grades": "Five Star"}}
        self.restaurants_col.update_one(_filter, update_operation)

    def update_many_restaurants(self):
        _filter = {"borough": "Hai Ba Trung"}
        update_operation = {"$set": {"borough": "Hanoi"}}
        self.restaurants_col.update_many(_filter, update_operation)

    # Delete
    def delete_one_restaurant(self, restaurant_id):
        _filter = {"restaurant_id": restaurant_id}
        self.restaurants_col.delete_one(_filter)

    def delete_many_restaurants(self, restaurant_ids):
        _filter = {"restaurant_id": {"$in": restaurant_ids}}
        self.restaurants_col.delete_many(_filter)
