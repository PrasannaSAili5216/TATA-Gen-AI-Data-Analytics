import pandas as pd
import sys

# Redirect stdout to a file
sys.stdout = open('eda_cleaned_results.txt', 'w', encoding='utf-8')

# Load the cleaned dataset
try:
    df = pd.read_csv('cleaned_dataset.csv')
except FileNotFoundError:
    print("Error: cleaned_dataset.csv not found. Please ensure the file is in the current directory.")
    exit()

print("--- INITIAL DATA TYPES (after preprocessing) ---")
print(df.dtypes)

# Data Cleaning & Type Conversion (redundant after preprocessing, but good to keep for consistency)
# We expect most of these to be clean now, but it handles potential new issues
numeric_cols = ['Age', 'Income', 'Credit_Score', 'Credit_Utilization',
                'Loan_Balance', 'Debt_to_Income_Ratio', 'Account_Tenure',
                'Delinquent_Account', 'Total_Problem_Payments'] # Updated numeric_cols

for col in numeric_cols:
    # Force numeric, coercing errors to NaN (should be minimal now)
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print("\n--- CLEANED DATA INFO (after preprocessing) ---")
print(df.info())

print("\n--- MISSING VALUES (after preprocessing) ---")
missing_counts = df.isnull().sum()
print(missing_counts[missing_counts > 0])
if missing_counts.sum() == 0:
    print("No missing values.")

print("\n--- SUMMARY STATISTICS (after preprocessing) ---")
print(df.describe())

print("\n--- DELINQUENCY CORRELATIONS (after preprocessing) ---")
if 'Delinquent_Account' in df.columns:
    correlations = df.corr(numeric_only=True)['Delinquent_Account'].sort_values(ascending=False)
    print(correlations)

print("\n--- CATEGORICAL ANALYSIS (after preprocessing) ---")
categorical_cols = ['Employment_Status', 'Credit_Card_Type', 'Location']
for col in categorical_cols:
    if col in df.columns:
        print(f"\nValue Counts for {col}:")
        print(df[col].value_counts(normalize=True))

# --- RISK INDICATORS DEEP DIVE (Updated for Total_Problem_Payments) ---
print("\n--- RISK INDICATORS DEEP DIVE (after preprocessing) ---")
# Check avg Credit Utilization for Delinquent vs Non-Delinquent
if 'Delinquent_Account' in df.columns and 'Credit_Utilization' in df.columns:
    print("\nAvg Credit Utilization by Delinquency:")
    print(df.groupby('Delinquent_Account')['Credit_Utilization'].mean())

# Check avg Total_Problem_Payments for Delinquent vs Non-Delinquent
if 'Delinquent_Account' in df.columns and 'Total_Problem_Payments' in df.columns:
    print("\nAvg Total_Problem_Payments by Delinquency:")
    print(df.groupby('Delinquent_Account')['Total_Problem_Payments'].mean())

# Check avg of 'Late' (1) and 'Missed' (2) for Delinquent vs Non-Delinquent in Month_X columns
month_cols = [f'Month_{i}' for i in range(1, 7)]
if 'Delinquent_Account' in df.columns and all(col in df.columns for col in month_cols):
    print("\nAverage Monthly Payment Status (0=On-time, 1=Late, 2=Missed) by Delinquency:")
    for month_col in month_cols:
        print(f"  {month_col}:")
        print(df.groupby('Delinquent_Account')[month_col].mean())
