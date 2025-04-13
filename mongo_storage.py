# Directory: PIIAgenticSystem/action_layer
# File: mongo_storage.py

import pymongo
from typing import Optional

class MongoHandler:
    def __init__(self, config):
        self.mongo_uri = config.mongo_uri
        self.database_name = config.database_name
        self.collection_name = config.collection_name

    def store_mapping_with_id(self, collection_id: str, masked_value: str, original_value: str) -> None:
        try:
            with pymongo.MongoClient(self.mongo_uri) as client:
                db = client[self.database_name]
                collection = db[self.collection_name]
                document = {
                    "collection_id": collection_id,
                    "masked_value": masked_value.strip("<>").strip(),
                    "original_value": original_value
                }
                collection.insert_one(document)
        except pymongo.errors.ConnectionFailure as e:
            print(f"Error storing to MongoDB: {e}")

    def retrieve_mapping_with_id(self, collection_id: str, masked_value: str) -> Optional[str]:
        try:
            with pymongo.MongoClient(self.mongo_uri) as client:
                db = client[self.database_name]
                collection = db[self.collection_name]
                document = collection.find_one({
                    "collection_id": collection_id,
                    "masked_value": masked_value.strip("<>").strip()
                })
                if document:
                    return document["original_value"]
                return None
        except pymongo.errors.ConnectionFailure as e:
            print(f"Error retrieving from MongoDB: {e}")
            return None

    def does_collection_id_exist(self, collection_id: str) -> bool:
        try:
            with pymongo.MongoClient(self.mongo_uri) as client:
                db = client[self.database_name]
                collection = db[self.collection_name]
                return collection.count_documents({"collection_id": collection_id}) > 0
        except pymongo.errors.ConnectionFailure as e:
            print(f"Error checking collection ID in MongoDB: {e}")
            return False