import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from urllib.parse import quote_plus

from src.models.api_model import APIModel

class MongoDBClass():
    def __init__(self, db_name, collection_name, mongo_uri=""):
        self.db_name = db_name
        self.collection_name = collection_name
        self.set_mongo_uri()

    def set_mongo_uri(self):
        load_dotenv()
        mongodb_username = os.getenv("MONGODB_USERNAME")
        mongodb_password = os.getenv("MONGODB_PASSWORD")
        mongodb_cluster_name = os.getenv("MONGODB_CLUSTER_NAME")
            # Escape the mongodb_username and mongodb_password
        mongodb_escaped_username = quote_plus(mongodb_username)
        mongodb_escaped_password = quote_plus(mongodb_password)

        # Construct the MongoDB Atlas URI
        mongo_uri = f"mongodb+srv://{mongodb_escaped_username}:{mongodb_escaped_password}@{mongodb_cluster_name}.mongodb.net"

        self.mongo_uri = mongo_uri


    def mongo_connect(self):
        try:
            # mongo config
            print(self.mongo_uri)

            client = MongoClient(self.mongo_uri)
            # Test the connection by accessing a database (e.g., admin)
            client.admin.command('ismaster')

            print("MongoDB Server Connected.")

            # Access the database
            db = client[self.db_name]

            # Check if the database exists
            db_list = client.list_database_names()
            if self.db_name in db_list:
                print(f"The {self.db_name} database exists.")
            else:
                print(f"The {self.db_name} database does not exist.")
                print(f"Creating {self.db_name} database.")
                db = client[self.db_name]

            # Access the collection
            collection_list = db.list_collection_names()
            if self.collection_name in collection_list:
                print(f"The {self.collection_name} collection exists.")
                collection = db[self.collection_name]
            else:
                print(f"The {self.collection_name} collection does not exist.")
                print(f"Creating {self.collection_name} collection.")
                collection = db[self.collection_name]

            return {"result": True, "message": collection}
            
        except ServerSelectionTimeoutError as err:
            print("MongoDB Server Connection Error:", err)
            return {"result": False, "message": "MongoDB Server Connection Error: " + str(err)}
        except Exception as e:
            print("An error occurred:", e)
            return {"result": False, "message": "An error occurred: " + str(e)}

    # def mongo_connect(self):
    #     # mongo config
    #     client = MongoClient(self.mongo_uri)
    #     if client is None:
    #         # no connection, exit early
    #         print("MongoDB Server Connection Error")
    #         return {"result": False ,"message": "MongoDB Server Connection Error."}
    #     else:
    #         print("MongoDB Server Connected.")
    #         # confirm oridosai db exist
    #         dblist = client.list_database_names()
    #         print(dblist)
    #         if self.db_name in dblist:
    #             print(f"The {self.db_name} database exists.")

    #             # confirm apis collection exist
    #             oridosai_db = client[self.db_name]
    #             collist = oridosai_db.list_collection_names()
    #             if self.collection_name in collist:
    #                 print(f"The {self.collection_name} collection exists.")
    #                 user_col = oridosai_db[self.collection_name]
    #                 return {"result": True, "message": user_col}
    #             else:
    #                 print(f"The {self.collection_name} collection not exists.")
    #                 return {"result": False ,"message": f"The {self.collection_name} collection not exists."}
    #         else:
    #             print(f"The {self.db_name} database does not exist.")
    #             # create the database
    #             client[self.db_name].create_collection(self.collection_name)
    #             print(f"The {self.db_name} database has been created with {self.collection_name} collection.")

    #             # confirm apis collection exist
    #             oridosai_db = client[self.db_name]
    #             collist = oridosai_db.list_collection_names()
    #             if self.collection_name in collist:
    #                 print(f"The {self.collection_name} collection exists.")
    #                 user_col = oridosai_db[self.collection_name]
    #                 return {"result": True, "message": user_col}
    #             else:
    #                 print(f"The {self.collection_name} collection not exists.")
    #                 return {"result": False ,"message": f"The {self.collection_name} collection not exists."}
                
    #             # return {"result": True, "message": f"The {self.db_name} database has been created with {self.collection_name} collection."}
    
    def create_api(self, data:APIModel):
        # Connect to MongoDB
        db = self.mongo_connect()

        if db["result"] == True:
            collection = db['message']

            # Insert the new document into the collection
            result = collection.insert_one(data)

            # Check if the insertion was successful
            if result.inserted_id:
                print("New item has been added to the collection with ID:", result.inserted_id)
                return True
            else:
                print("Failed to add a new item to the collection")
                return False
        else:
            return db 
        
    def delete_api(self, api_key, user):
        # Connect to MongoDB
        db = self.mongo_connect()

        if db["result"] == True:
            collection = db['message']

            # Define the filter condition to identify the document to delete
            filter_condition = {"api": api_key, "user": user}
            # Define the update operation
            update_operation = {"$set": { "is_removed": True }}

            # Update a single document that matches the filter condition
            result = collection.update_one(filter_condition, update_operation)
            if result.modified_count == 1:
                print("Document updated successfully")
            else:
                print("No matching document found")
        else:
            return db 
        
    def check_validation_api(self, api_key, user):
        # Connect to MongoDB
        db = self.mongo_connect()

        if db["result"] == True:
            collection = db['message']

            # Define the filter condition to check for document existence
            filter_condition = {"api": api_key, "user": user, "is_removed": False}

            # Check if a document exists that matches the filter condition
            existing_document = collection.find_one(filter_condition)
            if existing_document:
                print("Document exists in the collection")
                return True
            else:
                print("Document does not exist in the collection")
                return False
        else:
            return db 