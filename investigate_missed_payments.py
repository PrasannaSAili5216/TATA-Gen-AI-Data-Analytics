import pandas as pd

# Load the cleaned dataset
try:
    df = pd.read_csv('cleaned_dataset.csv')
except FileNotFoundError:
    print("Error: cleaned_dataset.csv not found. Please run preprocess_data.py first.")
    exit()

print("--- Missed_Payments Distribution by Delinquent_Account ---")
if 'Missed_Payments' in df.columns and 'Delinquent_Account' in df.columns:
    # Group by Delinquent_Account and then get value counts for Missed_Payments
    missed_payments_by_delinquency = df.groupby('Delinquent_Account')['Missed_Payments'].value_counts().unstack(fill_value=0)
    print(missed_payments_by_delinquency)

    print("\n--- Descriptive Statistics of Missed_Payments by Delinquent_Account ---")
    print(df.groupby('Delinquent_Account')['Missed_Payments'].describe())

    print("\n--- Examples where Missed_Payments are high but Delinquent_Account is 0 ---")
    # Filter for non-delinquent accounts with Missed_Payments > average for non-delinquent
    # We'll use a threshold that's clearly "high" based on the EDA
    # From EDA: Avg Missed Payments for non-delinquent is ~2.99
    # Let's pick Missed_Payments > 5 as an example of "high"
    high_missed_non_delinquent = df[(df['Delinquent_Account'] == 0) & (df['Missed_Payments'] > 5)]
    print(high_missed_non_delinquent[['Customer_ID', 'Missed_Payments', 'Delinquent_Account', 'Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']].head())

    print("\n--- Examples where Missed_Payments are low but Delinquent_Account is 1 ---")
    # Filter for delinquent accounts with Missed_Payments < average for delinquent
    # From EDA: Avg Missed Payments for delinquent is ~2.85
    # Let's pick Missed_Payments < 2 as an example of "low"
    low_missed_delinquent = df[(df['Delinquent_Account'] == 1) & (df['Missed_Payments'] < 2)]
    print(low_missed_delinquent[['Customer_ID', 'Missed_Payments', 'Delinquent_Account', 'Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']].head())

    print("\n--- Consistency Check: Missed_Payments vs Month_X columns ---")
    # Calculate actual missed payments from Month_1 to Month_6
    # '2' indicates a missed payment
    df['Calculated_Missed_Payments'] = df[['Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']].apply(
        lambda row: row.astype(str).str.count('2').sum(), axis=1
    )

    inconsistent_missed_payments = df[df['Missed_Payments'] != df['Calculated_Missed_Payments']]
    print(f"\nNumber of inconsistencies between 'Missed_Payments' and 'Month_X' columns: {len(inconsistent_missed_payments)}")

    if not inconsistent_missed_payments.empty:
        print("Examples of inconsistencies:")
        print(inconsistent_missed_payments[['Customer_ID', 'Missed_Payments', 'Calculated_Missed_Payments', 'Delinquent_Account', 'Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']].head())
    else:
        print("No inconsistencies found between 'Missed_Payments' and 'Month_X' columns.")

else:
    print("Required columns 'Missed_Payments' or 'Delinquent_Account' not found in the dataset.")
