import os
import sys 
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline,make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer,KNNImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelEncoder


from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger
from networksecurity.entity.artifact__entity import Data_Validation_Artifact,Data_Transformation_Artifact
from networksecurity.entity.config_entity import Data_transformation_config
from networksecurity.utils.main_utils.utils import save_ml_model,save_numpy_file,read_yaml_file,load_ml_model
from networksecurity.constant import training_pipeline


class Data_Transformation:
    def __init__(self,
                 input_artifact : Data_Validation_Artifact,
                 output_artifact : Data_transformation_config):
        try:
            self.input_artifact = input_artifact
            self.output_artifact = output_artifact
        except Exception as e:
            my_logger.info(f"Data Transformation Exception Occured: {e}")
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(data)->pd.DataFrame :
        try:
            return pd.read_csv(data)
        except Exception as e:
            my_logger.info(f"Data Transformation Exception Occured: {e}")
            raise NetworkSecurityException(e,sys)
        
    def data_transform_process(cls)-> Pipeline :
        try:
            argument : dict = read_yaml_file(training_pipeline.PARAMS_YAML_PATH)
            argument_knn = argument['knn_imputer']
            imputer : KNNImputer = KNNImputer()
            my_logger.info("my knn_imputer created")

            processor : Pipeline = Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            my_logger.error(f"Data Transformation Process Exception Occured: {e}")
            raise NetworkSecurityException(e,sys)
        
    def start_datatransformation (self) -> Data_Transformation_Artifact:
        try:
            my_logger.error("dattransformation starts ")

            train_file_path :str = self.input_artifact.valid_trin_file_Path
            test_file_path :str = self.input_artifact.valid_test_file_Path
            train_data = Data_Transformation.read_data(train_file_path)
            test_data = Data_Transformation.read_data(test_file_path)



            # my_logger.info(f"knn imputer data shape without drop {train_data.shape}")
            input_train_feature = train_data.drop(columns=training_pipeline.TARGET_COLUMN,axis=1)
            my_logger.critical(f" data cantain index {input_train_feature.columns}")
            my_logger.critical(f" data cantain index {input_train_feature.sample(2)}")
            my_logger.info("replacing in output feature -1 to 0 than only (1,0) cantain in output feature for classification problem")
            output_train_feature = (train_data[training_pipeline.TARGET_COLUMN]).replace(-1,0)

            input_test_feature = test_data.drop(columns=training_pipeline.TARGET_COLUMN,axis=1)
            output_test_feature = (test_data[training_pipeline.TARGET_COLUMN]).replace(-1,0)

            knn_imputer : Pipeline = self.data_transform_process()

            my_logger.info(f"knn imputer data shape {input_train_feature.shape}")

            imputer_object = knn_imputer.fit(input_train_feature)
            imputed_train_data = knn_imputer.transform(input_train_feature)
            imputed_test_data = knn_imputer.transform(input_test_feature)

            my_logger.info(f"ouur data is transformed and type {type(imputed_train_data)}........")


            traian_array = np.column_stack((imputed_train_data,np.array(output_train_feature)))
            test_array = np.column_stack((imputed_test_data,np.array(output_test_feature)))
            path_1= self.output_artifact.test_transformed_data

            print("aman path is : ",type(path_1),path_1)
            # my_logger(f" ::: {path_1}")

            save_numpy_file(test_array,path_1)
            save_numpy_file(data = traian_array,path = self.output_artifact.train_transformed_data)

            save_ml_model(model= imputer_object, path = self.output_artifact.transformed_output_file)

            my_logger.info(f"{type(imputer_object)}")

            save_ml_model( path ="final_model/preprocessor.pkl", model = imputer_object)



            output  = Data_Transformation_Artifact(
                transformed_train_file = self.output_artifact.test_transformed_data,
                transformed_test_file = self.output_artifact.train_transformed_data,
                transformed_output_file_path = self.output_artifact.transformed_output_file
            )
            my_logger.info ("all model are saved")
            return output


        except Exception as e:
            my_logger.info(f"start_datatransformation Exception Occured: {e}")
            raise NetworkSecurityException(e,sys)