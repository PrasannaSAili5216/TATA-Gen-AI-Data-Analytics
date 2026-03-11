# Tata Data Analytics Web Dashboard

This web application provides a user-friendly interface to interact with the data analytics and machine learning pipeline for the Tata Forage project. It allows you to preprocess data, train models, and evaluate bias without running command-line scripts manually.

## Features

- **Dataset Overview**: View summary statistics and a preview of the current dataset.
- **Preprocessing**: Trigger the data cleaning and feature engineering pipeline (`preprocess_data.py`).
- **Model Training**: Train Random Forest and Logistic Regression models and view performance metrics (`train_model.py`).
- **Bias Evaluation**: Run fairness analysis across different demographic groups (`evaluate_bias.py`).
- **Explainability**: Generate SHAP explanations for model predictions (`explain_model_shap.py`).
- **Real-time Logs**: View the output of the Python scripts directly in the web console.

## Prerequisites

- Python 3.x
- Flask
- Pandas, Scikit-learn, Imbalanced-learn (Imblearn)

## Installation

1. Ensure all dependencies are installed:
   ```bash
   pip install flask pandas scikit-learn imbalanced-learn
   ```

## Usage

1. Start the web server:
   ```bash
   python app.py
   ```
   *Note: If `python` is not in your path, try `py app.py`.*

2. Open your web browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. Use the dashboard buttons to execute the analysis steps in order:
   - **Preprocess Data** (Creates `cleaned_dataset.csv`)
   - **Train Model** (Trains and evaluates)
   - **Evaluate Bias** (Checks fairness)

## Project Structure

- `app.py`: Flask backend that orchestrates the Python scripts.
- `templates/index.html`: The main dashboard interface (HTML/JS).
- `static/css/styles.css`: Modern styling for the application.
- `preprocess_data.py`, `train_model.py`, `evaluate_bias.py`: original analysis scripts.
