from flask import Flask, render_template, request, redirect, url_for


from networksecurity.url_data.url_conversion import DomainInfo
from networksecurity.utils.main_utils.utils import load_ml_model
from networksecurity.utils.ml_utils.model.estimator import Network_model
from networksecurity.logging.logger import my_logger
from networksecurity.pipeline.training_pipeline import modeltraining_pipeline

import numpy as np



app = Flask("__name__")



@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/validate-url', methods=['GET', 'POST'])
# def validate_url():

#     if request.method == 'POST':
#         url = request.form['url']
#         obj_domain_info = DomainInfo()
#         result = obj_domain_info.extract_features(url)
#         return render_template(result)
        # Validate the URL here

@app.route('/validate-url', methods=['POST'])
def validate_url():
    if request.method == 'POST':
        url = request.form['url']
        obj_domain_info = DomainInfo()
        result = obj_domain_info.extract_features(url)

        my_logger.info(f"output of extract_features: {result}")
        # final_result = np.array(result).reshape(-1, 1)
        final_result = np.array(result, dtype=float).reshape(1, -1)

        my_logger.info(f"conver ed to numpy array: {final_result}")
        my_logger.info (f"shape of final result : {final_result.shape}")

        preprocessor = load_ml_model("final_model/preprocessor.pkl")
        ml_model = load_ml_model("final_model/best_model.pkl")

        model = Network_model(preprocessor= preprocessor, model=ml_model)
        prediction = model.predict(final_result)
        my_logger.info(f"model predict: {prediction}")

        prediction_label = "Malicious" if prediction[0] == 0 else "Benign"
        return render_template('result.html', prediction=prediction_label)
    return render_template('index.html')
        
@app.route('/train_model')
def train_model():
     train_obj = modeltraining_pipeline()
     train_obj.start_model_training()
     return "model trained successfully completes "





if __name__ == "__main__":
    app.run()