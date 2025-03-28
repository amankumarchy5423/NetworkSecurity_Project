import os 
import sys
import numpy as np
import pandas as pd
import datetime


PIPELINE_NAME = "networksecurity/constant/training_pipeline"
ARTIFACT_NAME : str = "networksecurity"
ARTIFACT_DIR : str = "Artifact"
FILE_NAME:str = "AmanData.csv"
TARGET_COLUMN = 'Result'
TRAINING_FILE_NAME = "train.csv"
TESTING_FILE_NAME = "test.csv"



DATA_INGESTION_COLLECTION_NAME:str = "aman_phisingData"
DATA_INGESTION_DATABASE_NAME:str = "aman_phising"

DATA_INGESTION_DIR_NAME :str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str = "feature_store"
DATA_INGESTION_INGESTED_DIR :str = "ingested"
DATA_TEST_SPLIT : float = 0.2




# NTWORK_DATA_DIR = "network_data"

SCHEMA_FILE_PATH = os.path.join('schema','schema.yaml')
DIFFERENCIATE_COLUMN = os.path.join('schema','categorized.yaml')
PARAMS_YAML_PATH = 'Params.yaml'

# TRAINING_PIPELINR_DIR = "networksecurity\constant\training_pipeline"
# DATA_INGUSION_PATH = "networksecurity\component\data_ingestion"

DATA_VALIDATION_DIRNAME :str = "DataValidation"
DATA_VALIDATION_VALID_DIR :str = "Valid"
DATA_VALIDATION_INVALID_DIR :str ="Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR :str = "DriftReport"
DATA_VALIDATION_DRIFT_FILE : str = "drift.json"



DATA_TRANSFORMATION_DIR = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = 'transformed_data'
DATA_TRANSFORMATION_OUTPUT_DIR = 'transformed_object'


