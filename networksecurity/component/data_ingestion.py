import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List

from sklearn.model_selection import train_test_split

from mlops_project_1.networksecurity.exception.exception import NetworkSecurityException
from mlops_project_1.networksecurity.logging.logger import my_logger
from mlops_project_1.networksecurity.entity.config_entity import Data_ingustion_config

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URI")

class Data_ingestion_mongo:
    def __init__(self,config_entity : Data_ingustion_config):
        try:
            self.data_config_entity = config_entity
        except Exception as e:
            my_logger.error(f"Data ingestion failed. Error: {str(e)}")
            raise NetworkSecurityException(e,sys) 
    
    def start_datengestion(self):
        try:
            data_base = self.data_config_entity.mongo_database_name
            collection = self.data_config_entity.mongo_collection_name

            self.client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
            my_logger.info("mongo client is successfully connected....")

            db = self.client["data_base"]
            collect = db['collection']

            data = collect.find()
            db = pd.DataFrame(list(data))

            if "_id" in db.columns.to_list():
                db = db.drop(columns=["_id"],axis=1,inplace=True)
            
            db.replace({"na": np.nan},inplace=True)

            return db

        except Exception as e:
            my_logger.error(f"Data ingestion failed. Error: {str(e)}")
            raise NetworkSecurityException(e,sys)