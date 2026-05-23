import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# 1. Load dataset
data = pd.read_csv("courier_data.csv")


# Convert categorical text (Traffic_Density) into numerical columns (0 and 1)
df= pd.get_dummies(data, columns=['Traffic_Density'], drop_first=True)

x = df.drop(columns=['Delivery_ID', 'Rider_ID', 'Burnout_Score'])
y = df['Burnout_Score']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

lr=LinearRegression()
rf=RandomForestRegressor(n_estimators=100, random_state=42)

lr_model=lr.fit(x_train,y_train)
rf_model=rf.fit(x_train,y_train)

lr_preds=lr_model.predict(x_test)
rf_preds=rf_model.predict(x_test)


print("--- Linear Regression Performance ---")
print(f"R2 Score: {r2_score(y_test, lr_preds):.4f}")
print(f"RMSE (Root Mean Squared Error): {np.sqrt(mean_squared_error(y_test, lr_preds)):.2f} points")


print("\n--- Random Forest Regressor Performance ---")
print(f"R2 Score: {r2_score(y_test, rf_preds):.4f}")
print(f"RMSE (Root Mean Squared Error): {np.sqrt(mean_squared_error(y_test, rf_preds)):.2f} points")

joblib.dump(rf_model, 'burnout_rf_model.pkl')

