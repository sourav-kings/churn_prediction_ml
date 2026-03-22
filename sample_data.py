"""
Generate sample customer data for training the churn prediction model.
"""

import pandas as pd
import numpy as np

def create_sample_data(num_samples=1000):
    """
    Create synthetic customer data with various features.
    Returns a DataFrame with customer information and churn labels.
    """
    np.random.seed(42)
    
    data = {
        'customer_id': range(1, num_samples + 1),
        'age': np.random.randint(18, 70, num_samples),
        'tenure_months': np.random.randint(1, 72, num_samples),
        'monthly_charges': np.random.uniform(20, 150, num_samples).round(2),
        'total_charges': np.random.uniform(100, 8000, num_samples).round(2),
        'num_services': np.random.randint(1, 8, num_samples),
        'contract_length': np.random.choice(['Month-to-month', 'One year', 'Two year'], num_samples),
        'has_support': np.random.choice([0, 1], num_samples),
        'payment_method': np.random.choice(['Credit card', 'Bank transfer', 'Mailed check'], num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (churn) with realistic patterns
    # Customers with low tenure, low services, or month-to-month contracts are more likely to churn
    churn_prob = (
        (1 - (df['tenure_months'] / 72)) * 0.3 +  # Higher probability for newer customers
        (1 - (df['num_services'] / 8)) * 0.2 +     # Higher probability for few services
        ((df['contract_length'] == 'Month-to-month').astype(int)) * 0.25 +
        np.random.uniform(0, 1, num_samples) * 0.25
    )
    df['churn'] = (churn_prob > 0.5).astype(int)
    
    return df

if __name__ == '__main__':
    df = create_sample_data(1000)
    df.to_csv('customer_data.csv', index=False)
    print(f"Sample data created with {len(df)} records")
    print(f"\nChurn distribution:\n{df['churn'].value_counts()}")
    print(f"\nFirst few rows:\n{df.head()}")
