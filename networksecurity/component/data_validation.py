from networksecurity.entity.config_entity import Data_validation_config
from networksecurity.entity.artifact__entity import Data_Validation_Artifact,data_engestion_output
from networksecurity.logging.logger import my_logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH,DIFFERENCIATE_COLUMN
from networksecurity.utils.main_utils.utils import read_yaml_file,read_data_fun,load_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
import json


class Data_Validation:
    def __init__(self, data_ingestion_out : data_engestion_output,
                 data_validation_config : Data_validation_config):
        try:
            self.data_input = data_ingestion_out
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            my_logger.exception(f"Data_Validation : {e}")
            raise NetworkSecurityException(e,sys) 
    
    def validate_no_column(self,dataframe :pd.DataFrame) -> bool:
        try:
            define_column = set(self.schema_config["columns"].keys())
            dataframe_columns = set(dataframe.columns)
            if not dataframe_columns.issubset(define_column):
                return False
            return True
        except Exception as e:
            my_logger.exception(f"validate_no_column : {e}")
            raise NetworkSecurityException(e,sys)
        
    def differenciate_colum(self,dataframe: pd.DataFrame) -> None:
        try:
            numeric_colum = []
            categorical_colum = []
            my_logger.info (f"start differenciate_colum :  {type(dataframe)}")
            for column in dataframe.columns:
                if dataframe[column].dtype in ['int64','float64']:
                    numeric_colum.append(column)
                else :
                    categorical_colum.append(column)
            
            column_cat = {
                "numeric_column" :numeric_colum,
                "categorical_columns" : categorical_colum
            }

            my_logger.info (f"column_cat :{type(column_cat)} {column_cat}")

            
            load_yaml_file(path =DIFFERENCIATE_COLUMN,data = column_cat)

        except Exception as e:
            my_logger.exception(f"find_numeric_colum : {e}")
            raise NetworkSecurityException(e,sys)
        
        
    def perform_DataDrift(self,
                          base_df : pd.DataFrame,
                          current_df : pd.DataFrame,
                          threshold = 0.5)->bool:
        try:
            status= True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1,d2)
                if is_sample_dist.pvalue < threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update({column :
                {"pvalue":is_sample_dist.pvalue,"drift_status":status}})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            drift_dir = os.path.dirname(drift_report_file_path)
            os.makedirs(drift_dir,exist_ok=True)

            my_logger.info(f"now its time to sumpt the report")

            with open(drift_report_file_path, "w") as file:
                 json.dump(report, file, indent=4)

        except Exception as e:
            my_logger.exception(f"perform_DataDrift : {e}")
            raise NetworkSecurityException(e,sys)


    def initiate_data_validation(self) -> Data_Validation_Artifact:
        try:
            train_file = self.data_input.train_file
            test_file = self.data_input.test_file

            my_logger.info("read data from train and test file")

            train_data = read_data_fun(train_file)
            test_data = read_data_fun(test_file)


            status = self.validate_no_column(train_data)
            if not status:
                msg = "hey column is missing in train file"
                my_logger.critical(msg)
                raise NetworkSecurityException(msg,sys)
            
            status1 = self.validate_no_column(test_data)
            if not status1:
                msg = "hey column is missing in test file"
                my_logger.critical(msg)
                raise NetworkSecurityException(msg,sys)

            my_logger.info("differnciate numerical and categorical colum")
            self.differenciate_colum(train_data)

            my_logger.info("check data drift .....")
            drift_report = self.perform_DataDrift(base_df=train_data,current_df=test_data)
            drift_report_path = self.data_validation_config.drift_report_file_path

            dir_name = os.path.dirname(drift_report_path)
            os.makedirs(dir_name,exist_ok=True)

            if drift_report is False :
                msg = "data drift is found"
                my_logger.critical(msg)
            else :
                valid_train_file = self.data_validation_config.data_valid_trainfile_path
                valid_test_file = self.data_validation_config.data_valid_testfile_path

                os.makedirs(os.path.dirname(valid_train_file),exist_ok=True)
                os.makedirs(os.path.dirname(valid_test_file),exist_ok=True)

                train_data.to_csv(valid_train_file,index = False)

                test_data.to_csv(valid_test_file, index=False)
            
            data_validation = Data_Validation_Artifact(
                    validation_status = drift_report,
                    valid_trin_file_Path = self.data_validation_config.data_valid_trainfile_path,
                    valid_test_file_Path = self.data_validation_config.data_valid_testfile_path,
                    invalid_trin_file_Path  = None,
                    invalid_test_file_Path  = None,
                    drift_report_file_path  = drift_report_path
            )
            return data_validation

        except Exception as e:
            my_logger.exception(f"initiate_data_validation : {e}")
            raise NetworkSecurityException(e,sys)
        