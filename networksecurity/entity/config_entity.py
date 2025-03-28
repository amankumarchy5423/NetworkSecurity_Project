from networksecurity.constant import training_pipeline 
from datetime import datetime
import os





class Train_pipeline_config :
    def __init__(self,timestamp = datetime.now()):
        self.timestamp = f"{timestamp.strftime('%d_%m_%y_%H_%M_%S')}"
        self.data_dir = training_pipeline.ARTIFACT_DIR
        self.training_pipe = training_pipeline.PIPELINE_NAME
        self.artifact_dir = os.path.join(self.data_dir,self.timestamp)
        self.timestamp : str = self.timestamp

class Data_ingustion_config():
    def __init__(self,config:Train_pipeline_config):
        self.data_ingestion_dir = os.path.join(
            config.data_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file = os.path.join(
            training_pipeline.DATA_INGESTION_DIR_NAME , training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        self.feature_store_dir = os.path.join(
            training_pipeline.DATA_INGESTION_DIR_NAME , training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
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


class Data_validation_config:
    def __init__(self,config : Train_pipeline_config):
        self.data_validation_config = config
        self.data_validation_dir : str = os.path.join(self.data_validation_config.artifact_dir , training_pipeline.DATA_VALIDATION_DIRNAME)

        self.valid_data_dir : str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir : str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.data_valid_testfile_path : str = os.path.join(
            self.valid_data_dir ,
            training_pipeline.DATA_VALIDATION_VALID_DIR,
            training_pipeline.TESTING_FILE_NAME
        )
        self.data_invalid_testfile_path : str = os.path.join(
            self.valid_data_dir ,
            training_pipeline.DATA_VALIDATION_INVALID_DIR,
            training_pipeline.TESTING_FILE_NAME
        )
        self.data_invalid_trainfile_path : str = os.path.join(
            self.valid_data_dir ,
            training_pipeline.DATA_VALIDATION_INVALID_DIR,
            training_pipeline.TRAINING_FILE_NAME
        )
        self.data_valid_trainfile_path : str = os.path.join(
            self.valid_data_dir ,
            training_pipeline.DATA_VALIDATION_VALID_DIR,
            training_pipeline.TRAINING_FILE_NAME
        )
        self.drift_report_file_path : str = os.path.join(
            self.data_validation_dir ,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_FILE
        )



class Data_transformation_config:
    def __init__(self,config : Train_pipeline_config):
        self.data_transformation_dir : str = os.path.join(config.artifact_dir , training_pipeline.DATA_TRANSFORMATION_DIR)
        self.train_transformed_data : str = os.path.join(
            self.data_transformation_dir , training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,(training_pipeline.TRAINING_FILE_NAME).replace('csv','npy')
        )
        self.test_transformed_data : str = os.path.join(
            self.data_transformation_dir , training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,(training_pipeline.TESTING_FILE_NAME).replace('csv','npy')
        )
        self.transformed_output_file : str = os.path.join(
            self.data_transformation_dir , training_pipeline.DATA_TRANSFORMATION_OUTPUT_DIR
        )



