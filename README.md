# Delinquency Prediction - EDA Project

This project performs Exploratory Data Analysis (EDA) on the Geldium delinquency dataset. It includes scripts to handle data corruption, clean the data (imputation), and generate a professional summary report.

## 1. Prerequisites
Ensure you have Python installed. Install the required libraries:

```bash
pip install pandas openpyxl python-docx
```

## 2. Project Scripts

### A. Data Cleaning (`inspect_data.py`)
This script is the **first step**. It:
1.  Manually extracts data from the corrupted `TASK_DETAILS/TASK_1/Delinquency_prediction_dataset.xlsx`.
2.  Standardizes categorical columns (e.g., Employment Status).
3.  Imputes missing values (Income, Loan Balance, Credit Score) using Median/Mean strategies.
4.  Saves the result to `cleaned_dataset.csv`.

**Run command:**
```bash
python inspect_data.py
```

### B. Report Generation (`generate_submission.py`)
This script contains the analysis findings and generates the final submission file. It strictly follows the provided template structure.

**Run command:**
```bash
python generate_submission.py
```
**Output:** `EDA_Summary_Report_Submission.docx` (Submit this file).

## 3. Other Files
*   `eda_analysis.py`: A helper script used during development to calculate correlations and statistics. You can run this if you want to see the raw numbers in the terminal.
*   `manual_extract.py`: The original recovery script (logic helps `inspect_data.py`).

## 4. How to Submit
1.  Run `python inspect_data.py` to verify data is clean.
2.  Run `python generate_submission.py` to create the report.
3.  Upload `EDA_Summary_Report_Submission.docx`.
