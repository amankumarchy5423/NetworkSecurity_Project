import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# MONGO_DB_URI = "mongodb+srv://amankumarchy5423:Aman5423@cluster0.jbrpl.mongodb.net/?appName=Cluster0"
# print(MONGO_DB_URI)

import certifi
ca = certifi.where()



import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException

MONGO_DB_URI = os.getenv('MONGODB_URI')
print(MONGO_DB_URI)

class Data_extract_network:
    def __init__(self):
        try :
            pass
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,path : Path):
        try :
            data = pd.read_csv(path)
            data.reset_index(drop=True,inplace=True)
            # record = list(json.loads(data.T.to_json()).values())
            record = data.to_dict(orient='record')     # both work same
            return record

        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def data_to_mongodb(self,data,database,collection):
        try :
            self.data = data
            self.database = database
            self.collection = collection

            logger.info("obj of mongodb client is made ")
            self.client = pymongo.MongoClient(MONGO_DB_URI)
            self.db = self.client[self.database]
            self.collection = self.db[self.collection]

            logger.info("now starting to insert data into mongodb")
            self.collection.insert_many(self.data)   # inser_many takes only dict and json format data
            logger.info("data inserted into mongodb")
            return "all set"
        
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        

if __name__ == "__main__" :
    data_path = "network_data/phisingData.csv"
    database = "aman_phising"
    collection = "aman_phisingData"
    obj = Data_extract_network()
    temp = obj.csv_to_json(data_path)
    report = obj.data_to_mongodb(temp,database,collection)
    print(report)
        

