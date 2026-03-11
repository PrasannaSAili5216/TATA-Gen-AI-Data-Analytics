# How to Run the Tata Data Analytics Dashboard (Step-by-Step)

This guide will walk you through setting up and running the web application for the Tata Data Analytics project.

## 1. Prerequisites (Skip if already installed)

Ensure you have Python installed. You can check by running `python --version` or `py --version` in your terminal.

You also need the following Python libraries installed:
- `flask` (for the web server)
- `pandas` (for data manipulation)
- `scikit-learn` (for machine learning)
- `imbalanced-learn` (for handling imbalanced data)
- `shap` (for model explainability)

To install them, run this command in your terminal:
```bash
pip install flask pandas scikit-learn imbalanced-learn shap
```

## 2. Start the Web Server

1. Open your terminal or command prompt.
2. Navigate to the project folder: `d:\Projects\Forage TATA Intern`
3. Run the following command to start the application:

   ```bash
   py app.py
   ```
   *(If `py` doesn't work, try `python app.py` or `python3 app.py`)*

4. You should see output similar to this, indicating the server is running:
   ```
    * Serving Flask app 'app'
    * Debug mode: on
    * Running on http://127.0.0.1:5000
   ```

## 3. Access the Dashboard

1. Open your web browser (Chrome, Edge, Firefox, etc.).
2. In the address bar, type: **http://127.0.0.1:5000**
3. Press Enter. The dashboard should load, filling your screen without scrollbars.

## 4. Using the Dashboard Workflow

Follow these steps in order to complete the analysis:

1. **Preprocess Data** (Click the `⚙️ Preprocess` button)
   - This cleans the raw data (`parsed_dataset.csv`), handles missing values, and creates `cleaned_dataset.csv`.
   - Wait for the "Completed preprocess successfully" message in the logs.

2. **Train Model** (Click the `🧠 Train Model` button)
   - This trains the Random Forest and Logistic Regression models.
   - The results (Accuracy, Precision, Recall) will appear in the "Terminal Logs" section at the bottom.

3. **Evaluate Bias** (Click the `⚖️ Evaluate Bias` button)
   - Checks the model's fairness across Age, Income, and Location groups.
   - A detailed report will be generated and shown in the logs.

4. **Explain (SHAP)** (Click the `🔍 Explain (SHAP)` button)
   - This generates a SHAP summary plot to visualize feature importance.
   - The plot will appear in the main visualization area in the center of the screen.

## Troubleshooting

- **Server won't start?** Check if another program is using port 5000.
- **Libraries missing?** Run the `pip install ...` command again.
- **Browser error?** Ensure the `py app.py` command is still running in the terminal. Do not close the terminal window while using the website.
