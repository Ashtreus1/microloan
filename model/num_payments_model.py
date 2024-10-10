import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

csv_file_path = 'data/data.csv'

# Load data from CSV file
if os.path.isfile(csv_file_path):
    df = pd.read_csv(csv_file_path)

    # Check if there is enough data to train the model
    if len(df) < 2:
        print("Not enough data to train the model. Please collect more data.")
        exit()

    # Features and target variable
    X = df[['loan_amount', 'expected_revenue']]
    y = df['num_payments_per_month']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'model/trained_payments_model.pkl')
else:
    print(f"CSV file not found: {csv_file_path}")
