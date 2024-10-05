import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

# Sample data (replace with your dataset)
data = {
    'loan_amount': [1000, 5000, 10000, 15000, 20000],
    'expected_revenue': [1500, 6000, 12000, 17000, 25000],
    'business_expenses': [500, 2000, 3000, 4000, 5000],
    'repayment_time': [1, 2, 3, 4, 5]  
}

df = pd.DataFrame(data)

# Features and target variable
X = df[['loan_amount', 'expected_revenue', 'business_expenses']]
y = df['repayment_time']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model

# joblib.dump(model, 'model/trained_model.pkl')
joblib.dump(model, 'trained_model.pkl')
