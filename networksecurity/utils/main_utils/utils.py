import yaml
import joblib
import os,sys
import numpy as np
import pandas as pd

# import dill
from ensure import ensure_annotations
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger


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

@ensure_annotations
def save_ml_model(model : object,path:str) -> None:
    try:
        if not os.path.exists(path):
              os.makedirs(os.path.dirname(path))
        else :
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
               
          