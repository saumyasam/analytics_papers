# -*- coding: utf-8 -*-
"""Predict_House_Price.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MQYIroQcdW4S2sFs23pHTrful4nfhtDo
"""

!pip install pandas numpy scikit-learn matplotlib seaborn statsmodels

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

train_data = pd.read_csv("/content/sample_data/train.csv")  # Replace with your file path
test_data = pd.read_csv("/content/sample_data/test.csv")    # Replace with your file path

train_data.head()
train_data.info()
train_data.describe()

sns.histplot(train_data['SalePrice'], kde=True)
plt.show()

# For numerical columns
for col in train_data.select_dtypes(include=np.number).columns:
    train_data[col] = train_data[col].fillna(train_data[col].median())

# For categorical columns
for col in train_data.select_dtypes(include='object').columns:
    train_data[col] = train_data[col].fillna(train_data[col].mode()[0])

train_data = pd.get_dummies(train_data)

# Example: Total square footage
train_data['TotalSF'] = train_data['TotalBsmtSF'] + train_data['1stFlrSF'] + train_data['2ndFlrSF']

import pandas as pd
import numpy as np
import statsmodels.api as sm

# ... (Your previous code for data loading, cleaning, and feature engineering) ...

# Convert all columns to numeric, coercing errors to NaN
X = X.apply(pd.to_numeric, errors='coerce')

# Fill NaN values after conversion (if any)
X = X.fillna(X.mean())  # or X.median(), depending on your preference

# Explicitly convert all columns to float
# This ensures all columns are numeric, addressing the error.
X = X.astype(float)

X = sm.add_constant(X)  # Add a constant term
model = sm.OLS(y, X).fit()
print(model.summary())

import statsmodels.formula.api as smf

# Get a list of dummy columns related to Neighborhood
neighborhood_cols = [col for col in train_data.columns if col.startswith('Neighborhood_')]

# Construct the formula using the dummy columns
formula = 'SalePrice ~ ' + ' + '.join(neighborhood_cols)

model_anova = smf.ols(formula, data=train_data).fit()
anova_table = sm.stats.anova_lm(model_anova)
print(anova_table)

residuals = model.resid
sns.histplot(residuals, kde=True)
plt.show()

from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_val)

# Random Forest Regressor
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_val)

# Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_val)

def evaluate_model(y_true, y_pred, model_name):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"{model_name} - RMSE: {rmse:.2f}, MAE: {mae:.2f}, R-squared: {r2:.2f}")

evaluate_model(y_val, y_pred_lr, "Linear Regression")
evaluate_model(y_val, y_pred_rf, "Random Forest")
evaluate_model(y_val, y_pred_gb, "Gradient Boosting")

neighborhood_columns = [col for col in train_data.columns if col.startswith('Neighborhood_')]
print(neighborhood_columns)

collgcr_avg_price = train_data[train_data['Neighborhood_CollgCr'] == 1]['SalePrice'].mean()
print(f"Average SalePrice in CollgCr: {collgcr_avg_price}")

# Calculate average sale prices by original neighborhood before one-hot encoding
# Assuming you have a copy of the original DataFrame before one-hot encoding
original_train_data = pd.read_csv("/content/sample_data/train.csv") # Assuming you kept a copy
location_prices = original_train_data.groupby('Neighborhood')['SalePrice'].mean()

# Now you can plot the data
location_prices.plot(kind='bar', figsize=(12, 6))
plt.title("Average Sale Price by Neighborhood")
plt.xlabel("Neighborhood")
plt.ylabel("Average Sale Price")
plt.show()