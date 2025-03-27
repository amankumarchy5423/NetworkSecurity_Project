import yaml
import pickle
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
