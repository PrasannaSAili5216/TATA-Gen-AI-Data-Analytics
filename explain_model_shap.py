
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

try:
    import shap
    print("SHAP library found.")
except ImportError:
    print("Error: SHAP library not installed. Please install it using 'pip install shap'.")
    exit(1)

# 1. Load Data
try:
    df = pd.read_csv('cleaned_dataset.csv')
except FileNotFoundError:
    print("Error: 'cleaned_dataset.csv' not found.")
    exit(1)

if 'Customer_ID' in df.columns:
    df = df.drop('Customer_ID', axis=1)

X = df.drop('Delinquent_Account', axis=1)
y = df['Delinquent_Account']

# 2. Preprocessing
# Use sparse_output=False to ensure dense arrays which are safer for SHAP
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    # Force dense output
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    verbose_feature_names_out=False # cleaner names
)

# 3. Train Model (Random Forest)
print("Preprocessing data...")
# Fit and transform
X_processed = preprocessor.fit_transform(X)
feature_names = preprocessor.get_feature_names_out()

# Split
print(f"Data shape: {X_processed.shape}")
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42, stratify=y)

# SMOTE
print("Applying SMOTE...")
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Train
print("Training Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_resampled, y_train_resampled)

# 4. SHAP Analysis
print("Calculating SHAP values...")
# TreeExplainer is fast for trees
explainer = shap.TreeExplainer(model)
# Calculate SHAP values for test set
shap_values = explainer.shap_values(X_test)

# Handle different SHAP output formats
if isinstance(shap_values, list):
    print(f"SHAP values returned as list of length {len(shap_values)}")
    # Class 1 (Delinquent) is index 1
    shap_vals_target = shap_values[1]
else:
    print(f"SHAP values returned as array of shape {shap_values.shape}")
    # If binary classification returns single array (rare for RF in sklearn), use it.
    # But usually RF returns list. If it's a regression model or boosted tree, it might be array.
    # For RF classifier, if it returns (samples, features, classes), it's 3D array in new SHAP versions.
    if len(shap_values.shape) == 3:
         shap_vals_target = shap_values[:, :, 1]
    else:
         shap_vals_target = shap_values

print(f"Target SHAP values shape: {shap_vals_target.shape}")

print("Generating SHAP summary plot...")
try:
    plt.figure()
    shap.summary_plot(shap_vals_target, X_test, feature_names=feature_names, show=False)
    plt.title("SHAP Feature Importance (Impact on Delinquency)")
    plt.tight_layout()
    plt.savefig('shap_summary_plot.png')
    print("Saved shap_summary_plot.png")
except Exception as e:
    print(f"Error generating plot: {e}")

# Calculate mean absolute SHAP values for text report
mean_abs_shap = np.mean(np.abs(shap_vals_target), axis=0)
sorted_indices = np.argsort(mean_abs_shap)[::-1]

print("\n--- Top 10 Features by SHAP Importance ---")
output_lines = []
output_lines.append("--- SHAP Feature Importance ---")
for i in range(min(10, len(feature_names))):
    idx = sorted_indices[i]
    if idx < len(feature_names):
        feat_name = feature_names[idx]
        importance = mean_abs_shap[idx]
        line = f"{i+1}. {feat_name}: {importance:.4f}"
        print(line)
        output_lines.append(line)

with open('shap_results.txt', 'w') as f:
    f.write("\n".join(output_lines))

print("\nSHAP analysis complete.")
