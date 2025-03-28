import yaml
import joblib
import os,sys
import numpy as np
import pandas as pd
import pickle

# import dill
from ensure import ensure_annotations
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


@ ensure_annotations
def read_yaml_file(path :str) -> dict:
    try:
        with open(path, 'r') as stream:
            data = yaml.safe_load(stream)
        return data
    except yaml.YAMLError as exc:
        my_logger.error(f"Error reading yaml file: {exc}")
        raise NetworkSecurityException(exc,sys)
    
# @ ensure_annotations
def load_yaml_file(path : str,data )-> None :
    try:
          with open(path, 'w') as stream:
               yaml.safe_dump(data, stream, default_flow_style=False)
    except Exception as e :
         my_logger.error(f"Error reading yaml file: {e}")
         raise NetworkSecurityException(e,sys)

    
@ ensure_annotations
def read_data_fun(data_pth) -> pd.DataFrame:
        try:
            return pd.read_csv(data_pth)
        except Exception as e:
            my_logger.exception(f"read data path : {e}")
            raise NetworkSecurityException(e,sys)

# @ensure_annotations
def save_ml_model(model : object,path:str) -> None:
    try:
        if not os.path.exists(path):
              os.makedirs(os.path.dirname(path),exist_ok=True)
        
        with open(path, 'wb') as f:
              joblib.dump(model, f)
    except Exception as e:
         my_logger.error(f"Error saving model: {e}")
         raise NetworkSecurityException(e,sys)

# @ensure_annotations
def save_numpy_file (data : np.array,path ) -> None:
     try:
            if not os.path.exists(path):
               os.makedirs(os.path.dirname(path),exist_ok=True)
            
            with open(path, 'wb') as f:
                 np.save(f, data)
     except Exception as e:
          my_logger.error(f"Error saving numpy file: {e}")
          raise NetworkSecurityException(e,sys)
     
def load_ml_model(model_path : str) -> object:
    try:
          if not os.path.exists(model_path):
               raise NetworkSecurityException("model path not found",sys)
          else :
               with open(model_path, 'rb') as f:
                    return joblib.load(f)
    except Exception as e:
         my_logger.error(f"Error loading model: {e}")
         raise NetworkSecurityException(e,sys)
    
def load_numpy_file(file_path : str)-> np.array:
    try:
          if not os.path.exists(file_path):
               raise NetworkSecurityException("file path not found",sys)
          else :
               with open(file_path, 'rb') as f:
                    return np.load(f)
    except Exception as e:
         my_logger.error(f"Error loading numpy file: {e}")
         raise NetworkSecurityException(e,sys)

# def evaluate_model(x_train,y_train,x_test,y_test,model,param):
#      try :
#         report = {}

#         for i in range(len(list(model))):
#                ml_models = list(model.values())[i]
#                model_params = param[list(model.keys())[i]]

#                gs = GridSearchCV(ml_models,model_params,cv=3)
#                gs.fit(x_train,y_train)

#                ml_models.set_params(**gs.best_params_)
#                ml_models.fit(x_train,y_train)

#                y_train_predict = ml_models.predict(x_train)
#                y_test_predict = ml_models.predict(x_test)
#             #    y_test_predict = ml_models.predict(y_train)

#                train_model_score = r2_score(y_train,y_train_predict)
#                test_model_score = r2_score(y_test,y_test_predict)

#                report[list(model.keys())[i]] = test_model_score
        
#         return report
        
            

#      except Exception as e:
#           my_logger.error(f"Error evaluating model: {e}")
#           raise NetworkSecurityException(e,sys)

# from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import r2_score

def evaluate_model(x_train, y_train, x_test, y_test, model, param):
    try:
        report = {}

        for i in range(len(list(model))):
            ml_models = list(model.values())[i]
            model_params = param.get(list(model.keys())[i], {})

            # Apply GridSearchCV only if parameters exist
            if model_params:
                gs = GridSearchCV(ml_models, model_params, cv=3)
                gs.fit(x_train, y_train.ravel())  # Ensure y_train is 1D
                ml_models.set_params(**gs.best_params_)

            # Fit the model
            ml_models.fit(x_train, y_train.ravel())

            # Predictions
            y_train_predict = ml_models.predict(x_train)
            y_test_predict = ml_models.predict(x_test)  # ✅ Corrected

            # Model performance
            train_model_score = r2_score(y_train, y_train_predict)
            test_model_score = r2_score(y_test, y_test_predict)

            # Store results
            report[list(model.keys())[i]] = test_model_score

        return report

    except Exception as e:
        my_logger.error(f"Error evaluating model: {e}")
        raise NetworkSecurityException(e, sys)

               
          