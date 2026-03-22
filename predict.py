"""
Make predictions using the trained churn model.
"""

import pandas as pd
import joblib
import numpy as np

class ChurnPredictor:
    """
    Load trained model and make churn predictions.
    """
    
    def __init__(self):
        """Load the trained model and preprocessing objects."""
        self.model = joblib.load('churn_model.pkl')
        self.scaler = joblib.load('scaler.pkl')
        self.label_encoders = joblib.load('label_encoders.pkl')
        self.feature_names = joblib.load('feature_names.pkl')
    
    def predict(self, customer_data):
        """
        Make prediction for a single customer.
        
        Args:
            customer_data: dict with keys:
                - age: int (18-70)
                - tenure_months: int (1-72)
                - monthly_charges: float
                - total_charges: float
                - num_services: int (1-8)
                - contract_length: str ('Month-to-month', 'One year', 'Two year')
                - has_support: int (0 or 1)
                - payment_method: str ('Credit card', 'Bank transfer', 'Mailed check')
        
        Returns:
            dict with prediction and probability
        """
        # Create DataFrame from input
        df = pd.DataFrame([customer_data])
        
        # Encode categorical variables
        df['contract_length'] = self.label_encoders['contract_length'].transform(
            df['contract_length']
        )
        df['payment_method'] = self.label_encoders['payment_method'].transform(
            df['payment_method']
        )
        
        # Scale numerical features
        numerical_cols = ['age', 'tenure_months', 'monthly_charges', 'total_charges', 'num_services', 'has_support']
        df[numerical_cols] = self.scaler.transform(df[numerical_cols])
        
        # Ensure column order matches training data
        df = df[self.feature_names]
        
        # Make prediction
        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0][1]
        
        return {
            'churn': bool(prediction),
            'churn_probability': float(probability),
            'no_churn_probability': float(1 - probability)
        }

if __name__ == '__main__':
    # Example usage
    predictor = ChurnPredictor()
    
    # Test with sample customer
    test_customer = {
        'age': 45,
        'tenure_months': 6,
        'monthly_charges': 75.50,
        'total_charges': 453.00,
        'num_services': 2,
        'contract_length': 'Month-to-month',
        'has_support': 0,
        'payment_method': 'Credit card'
    }
    
    result = predictor.predict(test_customer)
    print("\nPrediction Result:")
    print(f"Customer will churn: {result['churn']}")
    print(f"Churn probability: {result['churn_probability']:.2%}")
    print(f"No churn probability: {result['no_churn_probability']:.2%}")
