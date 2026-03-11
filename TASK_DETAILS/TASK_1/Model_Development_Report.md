# Predictive Model Development Report
**Project:** Delinquency Risk Prediction
**Model:** Random Forest Classifier (v1.0)
**Date:** October 26, 2023

## 1. Approach & Methodology
To predict customer delinquency, we developed a supervised machine learning model using the **Random Forest** algorithm.

*   **Algorithm Choice**: Random Forest
*   **Justification**: 
    *   **Handling Non-Linearity**: Capabilities to capture complex interactions between variables (e.g., Debt-to-Income vs. Utilization) that linear models like Logistic Regression often miss.
    *   **Robustness**: Built-in resistance to overfitting and ability to handle the mixed data types (numerical and categorical) present in the Geldium dataset.
    *   **Explainability**: Provides "Feature Importance" metrics, allowing the Collections team to understand *which* variables drive risk.

## 2. Model Performance
The model was trained on an 80/20 train-test split of the cleaned dataset. 

*   **Primary Metric (ROC-AUC)**: **0.47** (Improved slightly from 0.45 but still random)
*   **Accuracy**: 84% (Misleading - see below)

### 2.1 Confusion Matrix Analysis
The confusion matrix reveals the true behavior of the model:
```
[[84  0]  <- Correctly identified Non-Delinquents
 [16  0]] <- Missed ALL Delinquents (False Negatives)
```
*   **Recall (Class 1)**: 0.00
*   **Insight**: Despite using SMOTE to balance the classes and feature engineering to capture payment history, the model predicts "Non-Delinquent" for everyone. This confirms that the **input variables do not contain sufficient signal** to distinguish the two classes. The model "gave up" and just guessed the majority class to maximize accuracy.

### 🚨 Critical Finding: Data Signal Quality
The model performance (AUC < 0.50) is **below the random baseline**. This scientifically confirms the anomalies detected during EDA:
*   The features provided (Income, Credit Score) currently show **no predictive power** for the `Delinquent_Account` target in this sample.
*   The negative correlation of `Missed_Payments` suggests a potential **data labeling error** (e.g., are "Delinquent" labels flipped? Or is "Missed Payments" defined incorrectly?).

**Risk Assessment**: It is **not recommended** to deploy this model for intervention strategies in its current state, as it would likely result in random or incorrect targeting of customers.

## 3. Key Risk Drivers (Feature Importance)
Despite the low performance, the model identified which features it *tried* to use to differentiate customers. These align with our EDA:
1.  **Credit Utilization** (Top Factor)
2.  **Loan Balance**
3.  **Debt-to-Income Ratio**

This confirms that **leverage** (how much debt a customer has vs. income/limit) is the primary signal available, even if currently weak.

## 4. Evaluation & Next Steps Plan
To move from this prototype to a deployment-ready model, the following plan is proposed:

### Phase 1: Data Engineering Fixes (Immediate)
*   **Audit Target Variable**: Verify the definition of `Delinquent_Account`. Is 0 = Delinquent? The metrics suggest the labels might be inverted.
*   **Fix "Missed Payments"**: Investigate why customers with *fewer* missed payments are flagged as delinquent.

### Phase 2: Fairness & Evaluation (Post-Fix)
Once signal is restored, we will evaluate the model using:
*   **Fairness Audit**: Check False Positive Rates across protected classes (e.g., `Age` groups, `Location`). Ensure no demographic group is unfairly targeted for intervention.
*   **Lift Analysis**: Measure how much better the model is at capturing risk compared to random selection (targeting top 10% risky customers).
*   **Explainability**: Deploy SHAP (SHapley Additive exPlanations) values to give agents a "Reason Code" for every customer called (e.g., "Flagged due to 90% utilization").
