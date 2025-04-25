## END TO END ML PRODUCTION PROJECT ##

#  Network Security URL Classification

A Machine Learning-based solution to detect malicious URLs and protect users from phishing, malware, and other cyber threats.

 Built using MLflow, DVC, Flask, Docker & deployed on AWS EC2 with CI/CD integration.

---

##  Project Overview

This project classifies URLs as **legitimate or malicious** using a machine learning model trained on key security-related features. It includes end-to-end pipeline development, experiment tracking, and deployment, making it a complete MLOps-based solution.

---

##  Tech Stack

- **Languages**: Python, HTML  
- **ML & Data Tools**: Scikit-learn, Pandas, MLflow, DVC  
- **Web Framework**: Flask  
- **DevOps & Deployment**: Docker, GitHub Actions, AWS EC2, DagsHub

---

##  Machine Learning Workflow

### 1. **Data Ingestion**
- Collected and loaded a labeled dataset containing URLs with classifications (malicious or benign).
- Versioned raw data using DVC for reproducibility.

### 2. **Data Validation**
- Checked for missing values, incorrect formats, and duplicates.
- Ensured data schema consistency before transformation.

### 3. **Data Transformation**
- Extracted relevant features like:
  - Presence of IP address
  - HTTPS usage
  - URL length
  - Domain age
  - Number of special characters
- Saved transformation pipeline using `joblib` for reuse in production.

### 4. **Model Training**
- Trained multiple models: Logistic Regression, Random Forest, XGBoost.
- Tuned hyperparameters using cross-validation.
- Tracked all experiments, metrics, and parameters using **MLflow**.

### 5. **Model Evaluation**
- Evaluated models on multiple metrics: Accuracy, Precision, Recall, F1-Score.
- Chose the best model based on performance.
- Stored evaluation reports and model artifacts.

### 6. **Deployment**
- Built a user-friendly web interface using **Flask**.
- Dockerized the app for consistent deployment across platforms.
- Deployed on **AWS EC2** instance.
- Set up **CI/CD with GitHub Actions** for automated build and deployment.

---

## 🚀 How to Run the Project

### 🔧 Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/amankumarchy5423/NetworkSecurity_Project.git
cd NetworkSecurity_Project

# 2. Create and activate virtual environment
pip install uv
uv init
uv venv .venv
.venv\Scripts\activate         # On Windows


# 3. Install 

uv pip install -r requirements.txt

# 4. Start the Flask app
uv run app.py

# 5. Docerise the directory
docker build -t <image_name:tag> .

