"""
Flask API for real-time churn predictions with web UI.
"""

from flask import Flask, request, jsonify, render_template
from predict import ChurnPredictor
from sample_data import create_sample_data
import traceback
import random

app = Flask(__name__)

# Load predictor
predictor = ChurnPredictor()

app = Flask(__name__)

# Load predictor
predictor = ChurnPredictor()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def index():
    """Serve the web UI."""
    return render_template('index.html')

@app.route('/random-data', methods=['GET'])
def get_random_data():
    """Generate random customer data for UI."""
    try:
        # Generate a single sample and extract the data
        df = create_sample_data(1)
        customer_data = df.iloc[0].to_dict()

        # Remove customer_id and churn (not needed for prediction)
        customer_data.pop('customer_id', None)
        customer_data.pop('churn', None)

        # Convert numpy types to Python types
        for key, value in customer_data.items():
            if hasattr(value, 'item'):  # numpy types
                customer_data[key] = value.item()
            elif isinstance(value, float):
                customer_data[key] = round(value, 2)

        return jsonify({
            'customer_data': customer_data,
            'message': 'Random data generated successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make churn prediction for a customer.
    
    Expected JSON input:
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
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'age', 'tenure_months', 'monthly_charges', 'total_charges',
            'num_services', 'contract_length', 'has_support', 'payment_method'
        ]
        
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        result = predictor.predict(data)
        
        return jsonify({
            'prediction': result,
            'message': 'Prediction successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Make predictions for multiple customers.
    
    Expected JSON input:
    {
        "customers": [
            { customer1 data },
            { customer2 data }
        ]
    }
    """
    try:
        data = request.get_json()
        customers = data.get('customers', [])
        
        if not customers:
            return jsonify({'error': 'No customers provided'}), 400
        
        predictions = []
        for customer in customers:
            try:
                result = predictor.predict(customer)
                predictions.append({
                    'customer_data': customer,
                    'prediction': result
                })
            except Exception as e:
                predictions.append({
                    'customer_data': customer,
                    'error': str(e)
                })
        
        return jsonify({
            'predictions': predictions,
            'total': len(predictions),
            'successful': len([p for p in predictions if 'prediction' in p])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    print("Starting Churn Prediction API with Web UI...")
    print("🌐 Web UI: http://localhost:5000")
    print("🔗 API Endpoints:")
    print("- GET  /                    : Web interface")
    print("- GET  /health              : Check API status")
    print("- GET  /random-data         : Generate random customer data")
    print("- POST /predict             : Single prediction")
    print("- POST /predict/batch       : Batch predictions")

    app.run(debug=True, host='0.0.0.0', port=5000)
