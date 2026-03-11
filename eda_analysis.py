
import pandas as pd
import numpy as np

# Load the parsed dataset
df = pd.read_csv('parsed_dataset.csv')

print("--- INITIAL DATA TYPES ---")
print(df.dtypes)

# Data Cleaning & Type Conversion
numeric_cols = ['Age', 'Income', 'Credit_Score', 'Credit_Utilization', 'Missed_Payments', 
                'Loan_Balance', 'Debt_to_Income_Ratio', 'Account_Tenure', 'Delinquent_Account']

for col in numeric_cols:
    # Force numeric, coercing errors to NaN
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert Delinquent_Account to binary (0/1) just in case
# It might be read as numeric already, but ensure it

print("\n--- CLEANED DATA INFO ---")
print(df.info())

print("\n--- MISSING VALUES ---")
missing_counts = df.isnull().sum()
print(missing_counts[missing_counts > 0])

print("\n--- SUMMARY STATISTICS ---")
print(df.describe())

print("\n--- DELINQUENCY CORRELATIONS ---")
if 'Delinquent_Account' in df.columns:
    correlations = df.corr(numeric_only=True)['Delinquent_Account'].sort_values(ascending=False)
    print(correlations)

print("\n--- CATEGORICAL ANALYSIS ---")
categorical_cols = ['Employment_Status', 'Credit_Card_Type', 'Location']
for col in categorical_cols:
    if col in df.columns:
        print(f"\nValue Counts for {col}:")
        print(df[col].value_counts(normalize=True))

print("\n--- RISK INDICATORS DEEP DIVE ---")
# Check avg Credit Utilization for Delinquent vs Non-Delinquent
if 'Delinquent_Account' in df.columns and 'Credit_Utilization' in df.columns:
    print("\nAvg Credit Utilization by Delinquency:")
    print(df.groupby('Delinquent_Account')['Credit_Utilization'].mean())

# Check avg Missed Payments for Delinquent vs Non-Delinquent
if 'Delinquent_Account' in df.columns and 'Missed_Payments' in df.columns:
    print("\nAvg Missed Payments by Delinquency:")
    print(df.groupby('Delinquent_Account')['Missed_Payments'].mean())

