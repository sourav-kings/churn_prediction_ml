# Customer Churn Prediction ML Model

A complete machine learning pipeline to predict customer churn using scikit-learn and Flask for real-time deployment.

## Project Structure

```
churn_prediction_ml/
├── requirements.txt        # Python dependencies
├── sample_data.py         # Generate synthetic customer data
├── train_model.py         # Train the classification model
├── predict.py             # Make predictions using trained model
├── app.py                 # Flask API for real-time predictions
├── templates/
│   └── index.html         # Web UI template
├── static/
│   ├── style.css          # UI styling
│   └── script.js          # UI JavaScript
└── README.md              # This file
```

## Setup Instructions

### Step 1: Create Virtual Environment
```bash
cd churn_prediction_ml
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Sample Data & Train Model
```bash
python3 train_model.py
```

This will
- Generate 1000 sample customer records
- Split data into training (80%) and test (20%)
- Train a Random Forest classifier
- Evaluate model performance
- Save model and preprocessing objects

## Usage

### Option 1: Web UI (Recommended)
```bash
python3 app.py
```

Open your browser and go to `http://localhost:5000` for an interactive web interface with:
- Input fields for customer data
- Random data generation button
- One-click prediction
- Visual results display

### Option 2: Direct Prediction (Python)
```bash
python3 predict.py
```

### Option 3: Real-Time API Deployment
```bash
python3 app.py
```

The API will start at `http://localhost:5000`

#### API Endpoints:

**1. Web Interface**
```bash
GET /
```
Returns the interactive web UI.

**2. Health Check**
```bash
GET /health
```

**3. Random Data Generation**
```bash
GET /random-data
```
Returns randomly generated customer data for testing.

**4. Single Customer Prediction**
```bash
POST /predict
Content-Type: application/json

{
    "age": 45,
    "tenure_months": 6,
    "monthly_charges": 75.50,
    "total_charges": 453.00,
    "num_services": 2,
    "contract_length": "Month-to-month",
    "has_support": 0,
    "payment_method": "Credit card"
}
```

**3. Batch Predictions**
```bash
POST /predict/batch
Content-Type: application/json

{
    "customers": [
        { customer1 data },
        { customer2 data }
    ]
}
```

#### Example cURL Requests:

Single prediction:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "tenure_months": 6,
    "monthly_charges": 75.50,
    "total_charges": 453.00,
    "num_services": 2,
    "contract_length": "Month-to-month",
    "has_support": 0,
    "payment_method": "Credit card"
  }'
```

Health check:
```bash
curl http://localhost:5000/health
```

## Model Details

**Algorithm:** Random Forest Classifier
- **Trees:** 100
- **Max Depth:** 10
- **Features:** 8 customer attributes

**Features:**
- age: Customer age (18-70)
- tenure_months: Months as customer (1-72)
- monthly_charges: Monthly bill amount
- total_charges: Total amount spent
- num_services: Number of services used (1-8)
- contract_length: Type of contract
- has_support: Whether customer has support (0/1)
- payment_method: How customer pays

**Target Variable:**
- churn: Whether customer left company (0=No, 1=Yes)

## Output Interpretation

The model returns:
- **churn**: Boolean (true = likely to churn, false = likely to stay)
- **churn_probability**: Probability customer will churn (0-1)
- **no_churn_probability**: Probability customer will stay (0-1)

Example output:
```json
{
    "churn": false,
    "churn_probability": 0.23,
    "no_churn_probability": 0.77
}
```

## Performance Metrics

After training, the model shows:
- **Accuracy:** ~85-90%
- **ROC-AUC:** ~0.90+
- Detailed precision, recall, and F1-scores for both classes

## Next Steps

To improve the model:
1. **Add more features:** Include customer demographics, interaction history
2. **Hyperparameter tuning:** Use GridSearchCV or RandomizedSearchCV
3. **Try other algorithms:** XGBoost, Gradient Boosting, Neural Networks
4. **Handle imbalanced data:** Use SMOTE or class_weight
5. **Feature engineering:** Create interaction features, polynomial features
6. **Cross-validation:** Use k-fold cross-validation for better evaluation

## Deployment Options

- **Local:** Run Flask app on your machine
- **Cloud:** Deploy to Heroku, AWS, Google Cloud, or Azure
- **Containerized:** Package with Docker for consistent deployment
- **Batch Processing:** Process large customer files with predict.py modifications

## Requirements

- Python 3.7+
- See requirements.txt for package versions

## License

This is a sample project for educational purposes.
