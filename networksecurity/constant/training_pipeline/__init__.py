import os 
import sys
import numpy as np
import pandas as pd
import datetime

PIPELINE_NAME = "networksecurity\constant\training_pipeline"
ARTIFACT_NAME : str = "networksecurity"
ARTIFACT_DIR : str = "Artifact"
FILE_NAME:str = "AmanData.csv"

TRAINING_FILE_NAME = "train.csv"
TESTING_FILE_NAME = "test.csv"


DATA_INGESTION_COLLECTION_NAME:str = "aman_phisingData"
DATA_INGESTION_DATABASE_NAME:str = "aman_phising"

DATA_INGESTION_DIR_NAME :str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str = "feature_store"
DATA_INGESTION_INGESTED_DIR :str = "ingested"
DATA_TEST_SPLIT : float = 0.2




# NTWORK_DATA_DIR = "network_data"



# TRAINING_PIPELINR_DIR = "networksecurity\constant\training_pipeline"
# DATA_INGUSION_PATH = "networksecurity\component\data_ingestion"
