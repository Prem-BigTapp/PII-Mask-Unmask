# Directory: PIIAgenticSystem
# File: config.py

class Config:
    def __init__(self, mongo_uri="mongodb://localhost:27017/", database_name="pii_data", collection_name="pii_collection"):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.collection_name = collection_name