from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger
import sys
import os
import pandas as pd
from networksecurity.component.data_ingestion import Data_ingestion_mongo
from networksecurity.entity.artifact__entity import data_engestion_output,Data_Validation_Artifact
from networksecurity.entity.config_entity import Data_ingustion_config,Data_validation_config
from networksecurity.entity.config_entity import Train_pipeline_config
from networksecurity.component.data_validation import Data_Validation


if __name__ == "__main__":
    try:
        my_logger.info("<<<<< main.py >>>>>>")

        my_logger.info("Train_pipeline_config started >>>>>")
        obj3 = Train_pipeline_config()
        my_logger.info("Train_pipeline_config ended <<<<<")

        my_logger.info("Data_ingustion_config started >>>>>")
        obj2 = Data_ingustion_config(obj3)
        my_logger.info("Data_ingustion_config ended <<<<<")


        my_logger.info("Data_ingestion_mongo started >>>>>")
        obj = Data_ingestion_mongo(obj2)
        my_logger.info("Data_ingestion_mongo ended <<<<<")

        my_logger.info("Data ingestion mongo object is made")
        dataingestion_out = obj.initiate_data_ingestion()
        my_logger.info("Data ingestion function is initiated")

        my_logger.info("<<<<  start data validation  >>>>>")
        obj5 = Data_validation_config(obj3)

        obj4 = Data_Validation(dataingestion_out,obj5)

        data_validation_output=obj4.initiate_data_validation()

        my_logger.info("<<<<< main.py >>>>>>")
        # db = pd.read_csv("data_ingestion/data_ingestion/train.csv")
        # print(db.info())
    except Exception as e:
        my_logger.error(str(e))
        raise NetworkSecurityException(e,sys)
    



        
