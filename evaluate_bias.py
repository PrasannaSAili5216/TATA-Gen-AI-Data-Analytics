
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, f1_score, recall_score, precision_score

# 1. Load and Prepare Data
try:
    df = pd.read_csv('cleaned_dataset.csv')
except FileNotFoundError:
    print("Error: 'cleaned_dataset.csv' not found.")
    exit(1)

if 'Customer_ID' in df.columns:
    df = df.drop('Customer_ID', axis=1)

# Create Bias Analysis Groups BEFORE preprocessing (which encodes them)
# Age Groups
df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 50, 100], labels=['Young (<30)', 'Middle (30-50)', 'Senior (>50)'])

# Income Groups (using quantiles for fair distribution validation)
# Note: Income has missing values handled in preprocessing usually, but for group definition we need them.
# We will drop rows without Income for the *Income specific* bias check, or fillna for the general training.
# Let's fill NA for the groups definition to avoid dropping data, or just use what we have.
# The previous EDA imputed medians. Let's do a quick fill for group creation
df['Income_Filled'] = df['Income'].fillna(df['Income'].median())
df['Income_Group'] = pd.qcut(df['Income_Filled'], q=3, labels=['Low', 'Medium', 'High'])

# 2. Define Features and Target
X = df.drop(['Delinquent_Account', 'Age_Group', 'Income_Group', 'Income_Filled'], axis=1)
y = df['Delinquent_Account']

# Store groups for the test set alignment later
# We need to split groups exactly as we split X and y
X_indices = np.arange(len(X))
X_train_idx, X_test_idx, y_train, y_test = train_test_split(X_indices, y, test_size=0.2, random_state=42, stratify=y)

X_train = X.iloc[X_train_idx]
X_test = X.iloc[X_test_idx]

# Get the groups corresponding to the test set
test_groups_age = df.iloc[X_test_idx]['Age_Group']
test_groups_income = df.iloc[X_test_idx]['Income_Group']
test_groups_location = df.iloc[X_test_idx]['Location']

# 3. Preprocessing & Training
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier(n_estimators=200, random_state=42, min_samples_split=2))
])

print("Training Model...")
model.fit(X_train, y_train)

# 4. Predictions on Test Set
y_pred = model.predict(X_test)

# 5. Bias Analysis Function
def analyze_bias(y_true, y_pred, groups, group_name, file_handle):
    file_handle.write(f"\n--- Bias Analysis by {group_name} ---\n")
    results = []
    unique_groups = groups.unique()
    for g in unique_groups:
        try:
            mask = (groups == g)
            if mask.sum() == 0:
                continue
            
            y_test_g = y_true[mask]
            y_pred_g = y_pred[mask]
            
            recall = recall_score(y_test_g, y_pred_g, zero_division=0)
            precision = precision_score(y_test_g, y_pred_g, zero_division=0)
            f1 = f1_score(y_test_g, y_pred_g, zero_division=0)
            size = len(y_test_g)
            delinquency_rate = y_test_g.mean()
            
            output = f"Group: {g} (n={size})\n"
            output += f"  Recall (Sensitivity): {recall:.3f}\n"
            output += f"  Precision: {precision:.3f}\n"
            output += f"  F1 Score: {f1:.3f}\n"
            output += f"  Actual Delinquency Rate: {delinquency_rate:.3f}\n"
            file_handle.write(output)

            results.append({
                'Group': g,
                'Recall': recall,
                'Precision': precision,
                'F1': f1,
                'Size': size
            })
        except Exception as e:
            file_handle.write(f"Error processing group {g}: {e}\n")
    return results

# Run Analysis
print("Writing report to bias_report.txt...")
with open('bias_report.txt', 'w', encoding='utf-8') as f:
    f.write("=== BIAS EVALUATION REPORT ===\n")
    analyze_bias(y_test, y_pred, test_groups_age, 'Age Group', f)
    analyze_bias(y_test, y_pred, test_groups_income, 'Income Group', f)
    analyze_bias(y_test, y_pred, test_groups_location, 'Location', f)

print("Bias analysis complete.")
