from dataclasses import dataclass


@dataclass
class data_engestion_output:
    train_file : str
    test_file : str

@dataclass
class Data_Validation_Artifact:
    validation_status : bool
    valid_trin_file_Path : str
    valid_test_file_Path : str
    invalid_trin_file_Path : str
    invalid_test_file_Path : str
    drift_report_file_path : str

@dataclass
class Data_Transformation_Artifact:
    transformed_train_file : str
    transformed_test_file : str
    transformed_output_file_path : str

@dataclass
class Classification_artifact:
    f1_score : float
    precision : float
    recall : float

@dataclass
class Model_Training_Artifact:
    model_path : str
    train_metric_classification : Classification_artifact
    test_metric_classification : Classification_artifact
