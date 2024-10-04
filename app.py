from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('model/trained_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    loan_amount = float(request.form['loan_amount'])
    expected_revenue = float(request.form['expected_revenue'])

    # Predict repayment time in months and round to the nearest whole number
    prediction = model.predict(np.array([[loan_amount, expected_revenue]]))
    months = round(prediction[0])

    # Calculate repayment dates
    today = datetime.now()
    repayment_dates = []
    num_payments_per_month = 4  # For example, 4 payments (weekly)

    for month in range(months):
        for payment in range(num_payments_per_month):
            payment_date = today + timedelta(days=(30 * month) + (payment * (30 // num_payments_per_month)))
            repayment_dates.append(payment_date.strftime("%Y-%m-%d"))

    # Return the rendered template with JSON data
    return render_template('index.html', prediction=months, repayment_dates=repayment_dates)

if __name__ == '__main__':
    app.run(debug=True)
