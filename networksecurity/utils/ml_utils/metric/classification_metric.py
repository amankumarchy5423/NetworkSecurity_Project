from networksecurity.entity.artifact__entity import Classification_artifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import os,sys


def get_classification_report(y_true,y_predict)-> Classification_artifact:
    try:
        f1 = f1_score(y_true, y_predict)
        p1 = precision_score(y_true, y_predict)
        r1 = recall_score(y_true, y_predict)

        all_metric = Classification_artifact(
            f1_score=f1, precision=p1, recall=r1
        )
        return all_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
