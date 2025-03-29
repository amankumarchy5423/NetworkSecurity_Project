from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger
import sys
import os
import pandas as pd
from networksecurity.entity.artifact__entity import (data_engestion_output,
                                                     Data_Validation_Artifact,
                                                     Data_Transformation_Artifact,
                                                     Model_Training_Artifact)
from networksecurity.entity.config_entity import (Train_pipeline_config,
                                                  Data_ingustion_config,
                                                  Data_validation_config,
                                                  Data_transformation_config,
                                                  Model_training_config
                                                  )
from networksecurity.component.data_ingestion import Data_ingestion_mongo
from networksecurity.component.data_validation import Data_Validation
from networksecurity.component.data_transformation import Data_Transformation
from networksecurity.component.model_train import ModelTrainer
from networksecurity.cloud.s3_syncer import s3sync


TRANING_BUCKET_NAME = "networksecurity-bucket"

class modeltraining_pipeline:
    def __init__(self,train_pipeline_config = Train_pipeline_config()):
        try:
            self.train_pipeline_config = train_pipeline_config
            self.s3_sync = s3sync()
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)
    
    def start_data_ingestion(self):
        try:
           obj_data_ingestion =  Data_ingustion_config(self.train_pipeline_config)
           start_dataingestion = Data_ingestion_mongo(obj_data_ingestion)
           artifact_dataingestion=start_dataingestion.initiate_data_ingestion()
           return artifact_dataingestion
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self):
        try:
            data_ingestion_out = self.start_data_ingestion()
            obj_datavalidaton_config = Data_validation_config(self.train_pipeline_config)
            obj4 = Data_Validation(data_validation_config=obj_datavalidaton_config,data_ingestion_out=data_ingestion_out)
            data_validation_output=obj4.initiate_data_validation()
            return data_validation_output
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self):
        try:
            my_logger.critical("<==== Data transformation Starts ====>")
            
            data_validation_out = self.start_data_validation()
            datatransformation_config_obj = Data_transformation_config(self.train_pipeline_config)
            datatransformation_obj = Data_Transformation(input_artifact = data_validation_out,output_artifact=datatransformation_config_obj)
            data_transformation_output = datatransformation_obj.start_datatransformation()

            my_logger.critical("<==== Data transformation Endss ====>")
            return data_transformation_output
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)
        
    def sync_artifact_dir_to_s3(self):
        try:
            my_logger.critical("<==== Sync artifact dir to S3 started =====>")
            aws_bucket_url = f"s3://{TRANING_BUCKET_NAME}/artifact/{self.train_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder= self.train_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
            my_logger.critical("<==== Sync artifact dir to S3 ended =====>")
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)
    
    def sync_saved_model_dir(self):
        try:
            my_logger.critical("<==== Sync saved model dir to S3 started =====>")
            aws_bucket_url = f"s3://{TRANING_BUCKET_NAME}/final_model/{self.train_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder= self.train_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
            my_logger.critical("<==== Sync saved model dir to S3 ended =====>")
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)
        
    def start_model_training(self):
        try:
            my_logger.critical("<==== model training started =====>")
            
            data_transformation_output = self.start_data_transformation()
            model_training_config_obj = Model_training_config(self.train_pipeline_config)
            model_training_obj = ModelTrainer(model_trainer_config=model_training_config_obj,data_transformation_artifact=data_transformation_output)
            model_training_output = model_training_obj.initiate_training()

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir()

            my_logger.critical("<==== model training ended =====>") 
            # return model_training_output
        except Exception as e:
            my_logger.exception(e)
            raise NetworkSecurityException(e,sys)



# obj = modeltraining_pipeline()
