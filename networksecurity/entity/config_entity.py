from networksecurity.constant import training_pipeline 
from datetime import datetime
import os





class Train_pipeline_config :
    def __init__(self,timestamp = datetime.now()):
        self.timestamp = timestamp.strftime('%d_%m_%y_%H_%M_%S')
        self.data_dir = training_pipeline.ARTIFACT_DIR
        self.training_pipe = training_pipeline.PIPELINE_NAME
        self.artifact_dir = os.path.join(self.data_dir,timestamp)
        self.timestamp : str = timestamp

class Data_ingustion_config:
    def __init__(self,config:Train_pipeline_config):
        self.data_ingestion_dir = os.path.join(
            config.data_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_dir = os.path.join(
            training_pipeline.DATA_INGESTION_DIR_NAME , training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        self.data_training = os.path.join(
            training_pipeline.DATA_INGESTION_DIR_NAME,training_pipeline.DATA_INGESTION_DIR_NAME,training_pipeline.TRAINING_FILE_NAME
        )
        self.data_testing = os.path.join(
           training_pipeline.DATA_INGESTION_DIR_NAME,training_pipeline.DATA_INGESTION_DIR_NAME,training_pipeline.TESTING_FILE_NAME
        )
        self.data_testing_ratio = training_pipeline.DATA_TEST_SPLIT
        self.mongo_collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.mongo_database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME


