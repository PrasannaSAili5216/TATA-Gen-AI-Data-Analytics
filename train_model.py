
import sys

def check_imports():
    try:
        import pandas as pd
        import numpy as np
        import sklearn
        import imblearn
        return True
    except ImportError as e:
        print(f"Error: Missing required library. {e}")
        print("Please install requirements using: pip install pandas numpy scikit-learn")
        return False

if not check_imports():
    sys.exit(1)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

# 1. Load Data
try:
    df = pd.read_csv('cleaned_dataset.csv')
except FileNotFoundError:
    print("Error: 'cleaned_dataset.csv' not found. Please run 'inspect_data.py' first.")
    sys.exit(1)

# Drop ID columns (not predictive)
if 'Customer_ID' in df.columns:
    df = df.drop('Customer_ID', axis=1)

# 2. Define Features and Target
X = df.drop('Delinquent_Account', axis=1)
y = df['Delinquent_Account']

# 3. Preprocessing Pipeline
# Identify column types
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

print(f"Numeric Features: {list(numeric_features)}")
print(f"Categorical Features: {list(categorical_features)}")

# Numeric Transformer: Scale data
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Categorical Transformer: One-hot encode
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 4. Model Selection: Random Forest
# We use a Pipeline to ensure preprocessing is applied correctly to train/test
model_rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)), # Add SMOTE for oversampling
    ('classifier', RandomForestClassifier(n_estimators=200, random_state=42, min_samples_split=2))
])

# Model Selection: Logistic Regression
model_lr = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)), # Add SMOTE for oversampling
    ('classifier', LogisticRegression(solver='liblinear', random_state=42, class_weight='balanced'))
])

# 5. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("\nTraining Random Forest Model...")
model_rf.fit(X_train, y_train)

# 6. Evaluation - Random Forest
print("\n--- Random Forest Model Performance Evaluation ---")
y_pred_rf = model_rf.predict(X_test)
y_pred_proba_rf = model_rf.predict_proba(X_test)[:, 1]

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_rf))
print("\nClassification Report:")
print(classification_report(y_test, y_pred_rf))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba_rf):.4f}")

# 7. Explainability (Feature Importance) - Random Forest
rf_model = model_rf.named_steps['classifier']
# Feature names need to be obtained after preprocessing
preprocessed_feature_names_rf = preprocessor.get_feature_names_out()
all_feature_names_rf = preprocessed_feature_names_rf # Correctly assign feature names after preprocessing

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_rf))
print("\nClassification Report:")
print(classification_report(y_test, y_pred_rf))
recall_rf = classification_report(y_test, y_pred_rf, output_dict=True)['1']['recall']
print(f"Recall (Delinquent Class): {recall_rf:.4f}")
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba_rf):.4f}")

# 7. Explainability (Feature Importance) - Random Forest
rf_model = model_rf.named_steps['classifier']
