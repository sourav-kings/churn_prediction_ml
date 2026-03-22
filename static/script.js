// Customer Churn Prediction UI JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const randomBtn = document.getElementById('randomBtn');
    const predictBtn = document.getElementById('predictBtn');
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    const loadingDiv = document.getElementById('loading');

    // Random data generation
    randomBtn.addEventListener('click', function() {
        generateRandomData();
    });

    // Prediction
    predictBtn.addEventListener('click', function() {
        makePrediction();
    });

    // Generate random customer data
    function generateRandomData() {
        // Age: 18-70
        document.getElementById('age').value = Math.floor(Math.random() * (70 - 18 + 1)) + 18;

        // Tenure: 1-72 months
        document.getElementById('tenure_months').value = Math.floor(Math.random() * 72) + 1;

        // Monthly charges: $20-150
        document.getElementById('monthly_charges').value = (Math.random() * (150 - 20) + 20).toFixed(2);

        // Total charges: $100-8000
        document.getElementById('total_charges').value = (Math.random() * (8000 - 100) + 100).toFixed(2);

        // Number of services: 1-8
        document.getElementById('num_services').value = Math.floor(Math.random() * 8) + 1;

        // Contract length
        const contracts = ['Month-to-month', 'One year', 'Two year'];
        document.getElementById('contract_length').value = contracts[Math.floor(Math.random() * contracts.length)];

        // Has support: 0 or 1
        document.getElementById('has_support').value = Math.floor(Math.random() * 2);

        // Payment method
        const payments = ['Credit card', 'Bank transfer', 'Mailed check'];
        document.getElementById('payment_method').value = payments[Math.floor(Math.random() * payments.length)];

        // Show success message
        showResult('Random customer data generated successfully!', 'success');
        setTimeout(() => {
            hideResult();
        }, 2000);
    }

    // Make prediction
    function makePrediction() {
        // Validate form
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        // Collect form data
        const formData = new FormData(form);
        const customerData = {};

        for (let [key, value] of formData.entries()) {
            if (key === 'has_support') {
                customerData[key] = parseInt(value);
            } else if (['age', 'tenure_months', 'monthly_charges', 'total_charges', 'num_services'].includes(key)) {
                customerData[key] = parseFloat(value);
            } else {
                customerData[key] = value;
            }
        }

        // Show loading
        showLoading();

        // Make API request
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(customerData)
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();

            if (data.error) {
                showResult(`Error: ${data.error}`, 'warning');
                return;
            }

            // Display prediction result
            const prediction = data.prediction;
            const churnProb = (prediction.churn_probability * 100).toFixed(1);
            const noChurnProb = (prediction.no_churn_probability * 100).toFixed(1);

            let resultHTML = `
                <div class="churn-probability ${prediction.churn ? 'churn-yes' : 'churn-no'}">
                    ${prediction.churn ? '⚠️ HIGH RISK' : '✅ LOW RISK'}
                </div>
                <p><strong>Churn Probability:</strong> ${churnProb}%</p>
                <p><strong>Retention Probability:</strong> ${noChurnProb}%</p>
                <p><strong>Prediction:</strong> ${prediction.churn ? 'Customer likely to churn' : 'Customer likely to stay'}</p>
            `;

            showResult(resultHTML, prediction.churn ? 'warning' : 'success');
        })
        .catch(error => {
            hideLoading();
            showResult(`Network error: ${error.message}`, 'warning');
            console.error('Error:', error);
        });
    }

    // Utility functions
    function showLoading() {
        loadingDiv.classList.remove('hidden');
        predictBtn.disabled = true;
        randomBtn.disabled = true;
    }

    function hideLoading() {
        loadingDiv.classList.add('hidden');
        predictBtn.disabled = false;
        randomBtn.disabled = false;
    }

    function showResult(content, type) {
        resultContent.innerHTML = content;
        resultDiv.className = `result ${type}`;
        resultDiv.classList.remove('hidden');
    }

    function hideResult() {
        resultDiv.classList.add('hidden');
    }

    // Initialize with random data on page load
    setTimeout(() => {
        generateRandomData();
    }, 500);
});