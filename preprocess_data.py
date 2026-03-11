import pandas as pd
import numpy as np

# Load the dataset
try:
    df = pd.read_csv('parsed_dataset.csv')
except FileNotFoundError:
    print("Error: parsed_dataset.csv not found. Please ensure the file is in the current directory.")
    exit()

print("--- Original DataFrame Info ---")
df.info()

# --- 1. Standardize Employment_Status ---
print("\n--- Standardizing Employment_Status ---")
# Convert to lowercase and strip whitespace for consistent mapping
df['Employment_Status'] = df['Employment_Status'].astype(str).str.lower().str.strip()

# Map inconsistent values to standardized ones
status_mapping = {
    'employed': 'Employed',
    'emp': 'Employed',
    'self-employed': 'Self-Employed',
    'unemployed': 'Unemployed',
    'retired': 'Retired'
}
df['Employment_Status'] = df['Employment_Status'].map(status_mapping).fillna(df['Employment_Status'])

print("Value Counts for Employment_Status after standardization:")
print(df['Employment_Status'].value_counts())

# --- 2. Impute Missing Numerical Values ---
print("\n--- Imputing Missing Numerical Values ---")

# Impute Income with its median
if 'Income' in df.columns:
    income_median = df['Income'].median()
    df['Income'].fillna(income_median, inplace=True)
    print(f"Missing 'Income' values imputed with median: {income_median}")

# Impute Loan_Balance with its median
if 'Loan_Balance' in df.columns:
    loan_balance_median = df['Loan_Balance'].median()
    df['Loan_Balance'].fillna(loan_balance_median, inplace=True)
    print(f"Missing 'Loan_Balance' values imputed with median: {loan_balance_median}")

# Impute Credit_Score with its median
if 'Credit_Score' in df.columns:
    credit_score_median = df['Credit_Score'].median()
    df['Credit_Score'].fillna(credit_score_median, inplace=True)
    print(f"Missing 'Credit_Score' values imputed with median: {credit_score_median}")


# --- 3. Address Missed_Payments Inconsistency ---
print("\n--- Processing Missed_Payments and creating Total_Problem_Payments ---")

# Define mapping for Month_X columns
payment_status_map = {'On-time': 0, 'Late': 1, 'Missed': 2}
month_cols = [f'Month_{i}' for i in range(1, 7)]

# Apply mapping and convert to numeric
for col in month_cols:
    if col in df.columns:
        df[col] = df[col].map(payment_status_map).fillna(0).astype(int) # Fillna(0) for any unexpected values

# Calculate Total_Problem_Payments (sum of 'Late' and 'Missed' statuses)
df['Total_Problem_Payments'] = df[month_cols].apply(
    lambda row: sum(1 for x in row if x in [1, 2]), axis=1
)

# Drop the original Missed_Payments column as it's inconsistent
if 'Missed_Payments' in df.columns:
    df.drop('Missed_Payments', axis=1, inplace=True)
    print("Dropped original 'Missed_Payments' column.")

print("\n--- DataFrame Info after Imputation and Feature Engineering ---")
df.info()

print("\n--- Missing Values after all processing ---")
missing_counts_after = df.isnull().sum()
print(missing_counts_after[missing_counts_after > 0])
if missing_counts_after.sum() == 0:
    print("No missing values remaining in processed columns.")


# --- Save the cleaned dataset ---
output_file = 'cleaned_dataset.csv'
df.to_csv(output_file, index=False)
print(f"\nCleaned dataset saved to {output_file}")
