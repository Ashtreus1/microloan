from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained models
model_repayment = joblib.load('model/trained_repayment_model.pkl')
model_payments = joblib.load('model/trained_payments_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    loan_amount = float(request.form['loan_amount'])
    expected_revenue = float(request.form['expected_revenue'])
    payment_per_installment = float(request.form['payment_per_installment'])
    
    # Fixed interest rate logic based on loan amount
    if loan_amount <= 1000:
        interest_rate = 0.05  # 5% for smaller loans
    elif loan_amount <= 5000:
        interest_rate = 0.10  # 10% for medium loans
    else:
        interest_rate = 0.15  # 15% for larger loans

    # Predict repayment time in months and round to the nearest whole number
    prediction_repayment = model_repayment.predict(np.array([[loan_amount, expected_revenue]]))
    months = round(prediction_repayment[0])

    # Calculate total interest
    total_interest = loan_amount * interest_rate * (months / 12)
    
    # Total amount to be paid back
    total_repayment_amount = loan_amount + total_interest

    # Calculate total payments
    total_payments = total_repayment_amount / payment_per_installment

    # Calculate the number of payments per month
    payments_per_month = int(np.ceil(total_payments / months))

    # Calculate repayment dates starting after a week
    start_date = datetime.now() + timedelta(days=7)
    repayment_dates = []

    # Ensure we do not exceed the predicted repayment months
    for month in range(months):
        for payment in range(payments_per_month):
            # Check if all payments have been made
            if len(repayment_dates) >= total_payments:
                break
            payment_date = start_date + timedelta(days=(30 * month) + (payment * (30 // payments_per_month)))
            repayment_dates.append({
                'date': payment_date.strftime("%Y-%m-%d"),
                'amount': round(payment_per_installment, 2)
            })

    # Handle any remaining payments after even distribution
    remaining_payments = int(total_payments - len(repayment_dates))
    for payment in range(remaining_payments):
        if len(repayment_dates) >= total_payments:
            break
        payment_date = start_date + timedelta(days=(30 * (months - 1)) + (payment * (30 // remaining_payments)))
        repayment_dates.append({
            'date': payment_date.strftime("%Y-%m-%d"),
            'amount': round(payment_per_installment, 2)
        })

    # Prepare data for CSV
    data_to_save = {
        'loan_amount': loan_amount,
        'expected_revenue': expected_revenue,
        'payment_per_installment': payment_per_installment,
        'predicted_months': months,
        'total_repayment_amount': total_repayment_amount,
        'total_payments': total_payments,
        'num_payments_per_month': payments_per_month  
    }

    # Save the data to CSV
    csv_file_path = 'data/data.csv'
    
    # Create a DataFrame and append to CSV
    df = pd.DataFrame([data_to_save])
    
    # Check if the file exists to determine whether to write headers
    if not os.path.isfile(csv_file_path):
        df.to_csv(csv_file_path, mode='w', index=False)  
    else:
        df.to_csv(csv_file_path, mode='a', header=False, index=False) 

    # Return the rendered template with repayment dates and microloan amounts
    return render_template('index.html', prediction=months, repayment_dates=repayment_dates)

if __name__ == '__main__':
    app.run(debug=True)
