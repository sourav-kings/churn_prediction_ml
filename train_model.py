"""
Train the customer churn prediction model.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import joblib
from sample_data import create_sample_data

def prepare_data(df):
    """
    Prepare data for model training.
    - Handle missing values
    - Encode categorical variables
    - Scale numerical features
    """
    # Separate features and target
    X = df.drop(['customer_id', 'churn'], axis=1)
    y = df['churn']
    
    # Encode categorical variables
    categorical_cols = ['contract_length', 'payment_method']
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = ['age', 'tenure_months', 'monthly_charges', 'total_charges', 'num_services', 'has_support']
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    return X, y, scaler, label_encoders

def train_model(X_train, y_train):
    """
    Train Random Forest classifier for churn prediction.
    """
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance on test data.
    """
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("\n" + "="*50)
    print("MODEL EVALUATION RESULTS")
    print("="*50)
    print(f"\nAccuracy Score: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Churn', 'Churn']))

def main():
    """
    Main training pipeline.
    """
    print("Step 1: Creating sample data...")
    df = create_sample_data(1000)
    
    print("\nStep 2: Preparing data...")
    X, y, scaler, label_encoders = prepare_data(df)
    
    print("Step 3: Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    print("\nStep 4: Training model...")
    model = train_model(X_train, y_train)
    
    print("\nStep 5: Evaluating model...")
    evaluate_model(model, X_test, y_test)
    
    print("\nStep 6: Saving model and preprocessors...")
    joblib.dump(model, 'churn_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(label_encoders, 'label_encoders.pkl')
    joblib.dump(X.columns.tolist(), 'feature_names.pkl')
    
    print("\n✅ Model training complete!")
    print("Saved files: churn_model.pkl, scaler.pkl, label_encoders.pkl, feature_names.pkl")

if __name__ == '__main__':
    main()
