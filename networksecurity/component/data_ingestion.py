import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List

from sklearn.model_selection import train_test_split

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger
from networksecurity.entity.config_entity import Data_ingustion_config
from networksecurity.entity.dataengestion_entity import data_engestion_output

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

            # db = self.client[data_base]
            # collect = db[collection]
            collect=self.client[data_base][collection]

            data = collect.find()
            db = pd.DataFrame(list(data))

            print(db.sample(5))

            if "_id" in db.columns.to_list():
                db = db.drop(columns=["_id"],axis=1)
            
            # db.replace({"na": np.nan},inplace=True)

            return db

        except Exception as e:
            my_logger.error(f"Data ingestion failed. Error: {str(e)}")
            raise NetworkSecurityException(e,sys)
        
    def data_collection_to_feature(self,data : pd.DataFrame):
        try:

            feature_dir_path = self.data_config_entity.feature_store_dir
            feature_store_file_path = self.data_config_entity.feature_store_file
            my_logger.info("problem resolve ...")

            

            my_logger.info(f"{data.sample(2)}")
            my_logger.info(f"{feature_store_file_path}")

            os.makedirs(feature_dir_path,exist_ok=True)
            data.to_csv(path_or_buf=feature_store_file_path,index=False)
            # with open(feature_store_file_path,"w") as file:
            #     file.write(data.to_csv(index=False,header=True))
            my_logger.info("Data_ingestion_mongo.data_collection_to_feature completed >>>>>")

            # return data
        except Exception as e:
            my_logger.error(f"Data collection_to_db failed. Error: {str(e)}")
            raise NetworkSecurityException(e,sys)
        
    def data_train_test_csv(self,feature_collections : pd.DataFrame):
        try:

            train_file =self.data_config_entity.data_training
            test_file = self.data_config_entity.data_testing

            feature_collection = pd.DataFrame(feature_collections)

            print(feature_collection.sample())


            train,test = train_test_split(feature_collection,test_size=0.2)

            os.makedirs(os.path.dirname(train_file),exist_ok=True)

            my_logger.info("data is converted into train and test part...")
            train.to_csv(train_file,index = False ,header = True)
            test.to_csv(test_file,index = False,header = True)
            my_logger.info("data is converted into train and test file...")

            return train_file,test_file


        except Exception as e:
            my_logger.error(f"Data data_train_test_csv. Error: {str(e)}")
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.start_datengestion()
            self.data_collection_to_feature(dataframe)
            train,test = self.data_train_test_csv(dataframe)

            final_output=data_engestion_output(
                train_file=train,
                test_file=test
            )

            return final_output

        except Exception as e:
            my_logger.error(f"Data ingestion failed. Error: {str(e)}")
            raise NetworkSecurityException(e,sys)


        

