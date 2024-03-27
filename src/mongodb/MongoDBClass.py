import openai
import re
import os
import datetime
import jwt
import json
import pytz
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient

class MongoDBClass():
    def __init__(self, db_name, collection_name, mongo_uri=""):
        self.db_name = db_name
        self.collection_name = collection_name
        self.set_mongo_uri(mongo_uri)

    def set_mongo_uri(self, mongo_uri):
        if mongo_uri:
            self.mongo_uri = mongo_uri
        else:
            load_dotenv()
            self.mongo_uri = os.getenv("Mongo_URI")

        if self.mongo_uri is not None:
            os.environ["Mongo_URI"] = self.mongo_uri
            return True
        else:
            # Handle the absence of the environment variable
            # You might want to log an error, raise an exception, or provide a default value
            # For example, setting a default value
            os.environ["Mongo_URI"] = mongo_uri
            return False

    def mongo_connect(self):
        # mongo config
        client = MongoClient(self.mongo_uri)
        if client is None:
            # no connection, exit early
            print("MongoDB Server Connection Error")
            return {"result": False ,"message": "MongoDB Server Connection Error."}
        else:
            print("MongoDB Server Connected.")
            # confirm oridosai db exist
            dblist = client.list_database_names()
            if self.db_name in dblist:
                print(f"The {self.db_name} database exists.")

                # confirm apis collection exist
                oridosai_db = client[self.db_name]
                collist = oridosai_db.list_collection_names()
                if self.collection_name in collist:
                    print(f"The {self.collection_name} collection exists.")
                    user_col = oridosai_db[self.collection_name]
                    return {"result": True, "message": user_col}
                else:
                    print(f"The {self.collection_name} collection not exists.")
                    return {"result": False ,"message": f"The {self.collection_name} collection not exists."}
            else:
                print(f"The {self.db_name} database does not exist.")
                # create the database
                client[self.db_name].create_collection(self.collection_name)
                print(f"The {self.db_name} database has been created with {self.collection_name} collection.")
                return {"result": True, "message": f"The {self.db_name} database has been created with {self.collection_name} collection."}