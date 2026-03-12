# TATA Gen AI Data Analytics 📊

An end-to-end data science project demonstrating advanced analytics, predictive modeling, and AI explainability (XAI) as part of the **Tata Group Data Analytics** initiative.

---

## 🚀 Project Overview

This repository focuses on **predicting customer delinquency** for Geldium. The solution automates the journey from raw, corrupted data to professional business presentations and explainable AI insights.

---

## 📂 Project Classification & Structure

To make navigation easier, the project files are classified below:

### 🛠️ 1. Data Processing & Preparation
*   `inspect_data.py`: Main entry point for data recovery, cleaning, and imputation.
*   `preprocess_data.py`: Standardizes features and prepares data for modeling.
*   `extract_excel.py` & `manual_extract.py`: Robust scripts for handling corrupted XLSX files.
*   `investigate_missed_payments.py`: Granular analysis of missed payment patterns.

### 🧠 2. Predictive Modeling & AI
*   `train_model.py`: Trains the classification model to predict delinquency.
*   `evaluate_bias.py`: Checks for model fairness across different demographics.
*   `explain_model_shap.py`: Uses **SHAP (SHapley Additive exPlanations)** to provide transparent, feature-level insights into model decisions.

### 📈 3. Exploratory Data Analysis (EDA)
*   `eda_analysis_v2.py`: Generates statistical summaries and correlation matrices.
*   `peek_sheet.py`: Utility for quick data inspection.

### 📝 4. Automated Reporting & Deliverables
*   `generate_submission.py`: Produces the final Word-based EDA Summary Report.
*   `create_final_deck.py`: Generates the **Professional PowerPoint Presentation** using project findings.
*   `generate_final_report.py`: Orchestrates the consolidated project report.

---

## 🛠️ Getting Started

### Prerequisites
Install the required dependencies:
```bash
pip install pandas openpyxl python-docx python-pptx shap scikit-learn matplotlib seaborn
```

### Execution Flow
1.  **Clean Data**: `python inspect_data.py`
2.  **Train Model**: `python train_model.py`
3.  **Explain Logic**: `python explain_model_shap.py`
4.  **Generate Reports**: `python create_final_deck.py`

---

## ✨ Key Features
*   **Bias Mitigation**: Demographic parity checks ensure fair lending predictions.
*   **Professional Automation**: Direct conversion of data insights into boardroom-ready PPTX slides.

---
*Created for the Tata Group Forage Intern Program.*
