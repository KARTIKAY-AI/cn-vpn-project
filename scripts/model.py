import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Load the feature-engineered dataset
df = pd.read_csv('results/dataset_features.csv')

df = df.dropna(subset=['throughput_mbps'])

# Select input features
X = pd.get_dummies(
    df[['vpn', 'rtt_ms', 'loss_pct']],
    columns=['vpn']
)

# Target variable
y = df['throughput_mbps']

# Split data into training and testing sets
Xtr, Xte, ytr, yte = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42
)

# Train Random Forest Regression model
m = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

m.fit(Xtr, ytr)

# Make predictions
p = m.predict(Xte)

# Evaluate model
print('R2 on held-out data:', round(r2_score(yte, p), 3))

print('MAE (Mbit/s):', round(mean_absolute_error(yte, p), 1))

# Display feature importance
print('Feature importance:')

print(
    dict(
        zip(
            X.columns,
            m.feature_importances_.round(3)
        )
    )
)

