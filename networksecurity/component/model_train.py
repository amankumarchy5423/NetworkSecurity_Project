from networksecurity.logging.logger import my_logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import training_pipeline
from networksecurity.entity.artifact__entity import Classification_artifact,Model_Training_Artifact,Data_Transformation_Artifact
from networksecurity.entity.config_entity import Model_training_config
from networksecurity.utils.main_utils.utils import load_numpy_file,save_numpy_file,load_ml_model
from networksecurity.utils.main_utils.utils import evaluate_model,save_ml_model
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_report
from networksecurity.utils.ml_utils.model.estimator import Network_model


import mlflow
import os,sys
import numpy as np
import pandas as pd 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)



# mlflow.set_tracking_uri(uri='http://127.0.0.1:5000')
# mlflow.set_experiment(experiment_name="Network Security Experiment")

# mlflow.sklearn.autolog()

class ModelTrainer:
    def __init__(self,
                 model_trainer_config :Model_training_config,
                 data_transformation_artifact : Data_Transformation_Artifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            my_logger.error(f"An error occurred: {str(e)}")
            raise NetworkSecurityException(e,sys) 
    
    def mlfow_connection(self,best_model,classifier_report):
        try:
            with mlflow.start_run():
                f1 = classifier_report.f1_score
                precision = classifier_report.precision
                recall = classifier_report.recall

                mlflow.log_metric(key="f1_score",value=f1)
                mlflow.log_metric(key="precision",value=precision)
                mlflow.log_metric(key="recall",value=recall)
                mlflow.sklearn.log_model(best_model,"best_model")
        except Exception as e:
            my_logger.error(f"An error occurred: {str(e)}")
            raise NetworkSecurityException(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models = {
            "Logistic Regression" : LogisticRegression(),
            # "knn_model" : KNeighborsClassifier(n_neighbors=5),
            "Random Forest" : RandomForestClassifier(verbose=1),
            "Decision Tree" : DecisionTreeClassifier(),
            "Gradient Boosting" : GradientBoostingClassifier(verbose=1),
            "AdaBoost" : AdaBoostClassifier()
            }

            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
             }
            model_report : dict = evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test
                                                 ,model=models,param=params)
            
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            y_train_predict = best_model.predict(x_train)
            classification_train_metric = get_classification_report(y_true=y_train,y_predict=y_train_predict)

            my_logger.info("my best model is %s with score %f" % (best_model_name, best_model_score))

            y_test_predict = best_model.predict(x_test)
            classification_test_metric = get_classification_report(y_true=y_test,y_predict=y_test_predict)
            
            my_logger.info("my best model and matrix is loged in mlflow")
            self.mlfow_connection(best_model=best_model,classifier_report=classification_train_metric)
            self.mlfow_connection(best_model=best_model,classifier_report=classification_test_metric)

            my_logger.info("now its time for load our model")
            my_logger.info(f"file path where error cause : {self.data_transformation_artifact.transformed_output_file_path}")
            my_logger.info(f"File Exists: {os.path.exists(self.data_transformation_artifact.transformed_output_file_path)}")
            # my_logger.info(f"File Size: {os.path.getsize(self.data_transformation_artifact.transformed_output_file_path)} bytes")
              # Should not be 0
            data_preprocessor_pipe = load_ml_model(self.data_transformation_artifact.transformed_output_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.model_trained_file)
            os.makedirs(model_dir_path,exist_ok=True)
 
            my_logger.info("model are loade and ready to use")
            Network_model_obj=Network_model(preprocessor = data_preprocessor_pipe,model = best_model)
            save_ml_model(path = self.model_trainer_config.model_trained_file,model=Network_model_obj)

            model_train_artifact=Model_Training_Artifact(model_path=self.model_trainer_config.model_trained_file,
                                   train_metric_classification=classification_train_metric ,
                                    test_metric_classification=classification_test_metric )
            
            my_logger.info("model loaded and saved")
            return model_train_artifact

            

        except Exception as e:
            my_logger.error(f"An error occurred: {str(e)}")
            raise NetworkSecurityException(e,sys)


    def initiate_training(self)->Model_Training_Artifact:
        try :
            
            train_file_path : str = self.data_transformation_artifact.transformed_train_file
            test_file_path :str = self.data_transformation_artifact.transformed_test_file

            train_data: np.array = load_numpy_file(file_path=train_file_path)
            test_data: np.array = load_numpy_file(file_path=test_file_path)

            x_train,y_train,x_test,y_test = (
                train_data[:,:-1],train_data[:,-1].reshape(-1, 1),
                test_data[:,:-1],test_data[:,-1].reshape(-1, 1)
            )

            my_logger.info(f"train_data : {x_train.shape} , {y_train.shape}")
            my_logger.info(f"test_data : {x_test.shape} , {y_test.shape}")
            # my_logger.info(x_train[1])
            # my_logger.info(f"x_test data======{x_test[1:10]} \n")
            # my_logger.info(y_train[1])
            # my_logger.info(f"y_test data ==== {y_test[1:10]}")

            model_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_artifact

        except Exception as e:
            my_logger.error(f"An error occurred: {str(e)}")
            raise NetworkSecurityException(e,sys)



