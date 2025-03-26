from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger
import sys
import os
from networksecurity.component.data_ingestion import Data_ingestion_mongo
from networksecurity.entity.dataengestion_entity import data_engestion_output
from networksecurity.entity.config_entity import Data_ingustion_config
from networksecurity.entity.config_entity import Train_pipeline_config


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
        out = obj.initiate_data_ingestion()
        my_logger.info("Data ingestion function is initiated")

        my_logger.info("<<<<< main.py >>>>>>")
        print(out)
    except Exception as e:
        my_logger.error(str(e))
        raise NetworkSecurityException(e,sys)
    



        
