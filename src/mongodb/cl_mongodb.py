import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from urllib.parse import quote_plus

from src.models.api_model import APIModel

class MongoDB():
    def __init__(self, db_name, collection_name, mongo_uri=""):
        """Initialize the MongoDB with the database and collection names.

        Args:
        - db_name (str): Name of the MongoDB database.
        - collection_name (str): Name of the collection within the database.
        - mongo_uri (str, optional): MongoDB connection URI.
        """
        self.db_name = db_name
        self.collection_name = collection_name
        self.__set_mongo_uri()

    def __set_mongo_uri(self):
        """Set the MongoDB connection URI using environment variables."""
        load_dotenv()
        mongodb_username = os.getenv("MONGODB_USERNAME")
        mongodb_password = os.getenv("MONGODB_PASSWORD")
        mongodb_cluster_name = os.getenv("MONGODB_CLUSTER_NAME")
            # Escape the mongodb_username and mongodb_password
        mongodb_escaped_username = quote_plus(mongodb_username)
        mongodb_escaped_password = quote_plus(mongodb_password)

        # Extract MongoDB URI from payload data
        mongo_uri = f"mongodb+srv://{mongodb_escaped_username}:{mongodb_escaped_password}@{mongodb_cluster_name}.mongodb.net"

        self.mongo_uri = mongo_uri


    def __mongo_connect(self):
        """Connect to the MongoDB server and database, and get the specified collection."""
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

    # def __mongo_connect(self):
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
    