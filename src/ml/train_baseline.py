import pandas as pd
import numpy as np
import os
import json
import joblib
from datetime import datetime, timezone

from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler

class TrainingModels():
    def __init__(self, ml_csv_path:str) -> None:
        if not os.path.exists(ml_csv_path):
            raise FileNotFoundError("FILE NOT FOUND")
        print("TrainingModels.__init__: dataset loaded")
        
        self.ml_csv_path = ml_csv_path
    
    def _prepare_data(self) -> None:
        df = pd.read_csv(self.ml_csv_path, sep=";")

        target = "global_active_power"

        X = df.drop(columns=[target])
        y = df[target]

        split_idx = int(len(df) * 0.7)

        self.X_train, self.X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        self.y_train, self.y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        print("TrainingModels._prepare_date: data splitted and scaled")

    def _ridge_train(self) -> None:
        self.ridge_model = Ridge(alpha=1.0)
        self.ridge_model.fit(self.X_train_scaled, self.y_train)
        print("TrainingModels._ridge_train: ridge model trained")

        y_pred = self.ridge_model.predict(self.X_test_scaled)
        print("TrainingModels._ridge_train: ridge model prediction done")

        self.rmse_ridge = np.sqrt(mean_squared_error(self.y_test, y_pred))
        self.mae_ridge = mean_absolute_error(self.y_test, y_pred)
    
    def _linear_train(self) -> None:
        self.linear_model = LinearRegression()
        self.linear_model.fit(self.X_train_scaled, self.y_train)
        print("TrainingModels._linear_train: linear model trained")

        y_pred = self.linear_model.predict(self.X_test_scaled)
        print("TrainingModels._linear_train: linear model prediction done")

        self.rmse_linear = np.sqrt(mean_squared_error(self.y_test, y_pred))
        self.mae_linear = mean_absolute_error(self.y_test, y_pred)

    def train_models(self) -> None:
        self._prepare_data()
        self._ridge_train()
        self._linear_train()

    def report(self) -> None:
        print("Ridge Regression Results")
        print(f"RMSE: {self.rmse_ridge:.4f}")
        print(f"MAE : {self.mae_ridge:.4f}")

        print("Linear Regression Results")
        print(f"RMSE: {self.rmse_linear:.4f}")
        print(f"MAE : {self.mae_linear:.4f}")

    def save_models(self, output_dir:str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        
        joblib.dump(self.ridge_model, os.path.join(output_dir, "ridge_model.joblib"))
        joblib.dump(self.linear_model, os.path.join(output_dir, "linear_model.joblib"))
        joblib.dump(self.scaler, os.path.join(output_dir, "scaler.joblib"))
        print(f"TrainingModels.save_models: models were saved at {output_dir}")

    def save_metrics(self, output_path:str) -> None:
        metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ridge": {
                "rmse": self.rmse_ridge,
                "mae": self.mae_ridge,
                "alpha": 1.0
            },
            "linear": {
                "rmse": self.rmse_linear,
                "mae": self.mae_linear
            }
        }
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=4)
        print(f"TrainingModels.save_metrics: metrics were saved at {output_path}")