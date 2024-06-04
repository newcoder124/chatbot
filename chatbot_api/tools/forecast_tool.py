from prophet import Prophet
from datetime import datetime
import pandas as pd
import json

def forecast_time_series(data: str) -> str:
    try:
        # Load the data
        history = pd.read_json(data)
        
        # Prepare the data for Prophet
        X = history.rename(columns={"date": "ds", "value": "y"})
        
        # Fit the model
        model = Prophet()
        model.fit(X)
        
        # Make a future dataframe for predictions
        future = model.make_future_dataframe(periods=12, freq='M')  # Forecast for next 30 days
        forecast = model.predict(future).iloc[history.shape[0]:, :]
        
        # Prepare the output
        forecast = forecast.rename(columns={'ds': 'date', 'yhat': 'forecast'})
        history = history.rename(columns={'value': 'history'})
        output = forecast.merge(history, on='date', how='outer')
        output = output[['date','history','forecast']].sort_values('date')
        return output
    
    except Exception as e:
        return json.dumps({"error": str(e)})

# def forecast_time_series(data: str) -> str:
#     try:
#         # Load the data
#         df = pd.read_json(data)
        
#         # Prepare the data for Prophet
#         df.rename(columns={"date": "ds", "value": "y"}, inplace=True)
        
#         # Fit the model
#         model = Prophet()
#         model.fit(df)
        
#         # Make a future dataframe for predictions
#         future = model.make_future_dataframe(periods=30)  # Forecast for next 30 days
#         forecast = model.predict(future)
        
#         # Prepare the output
#         forecast_output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
#         # return forecast_output
#         return forecast_output.to_json(orient="records")
    
#     except Exception as e:
#         return json.dumps({"error": str(e)})

ts_data = """{"date": ["2022-10-01", "2022-11-01", "2022-12-01", "2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01", "2023-06-01", "2023-07-01", "2023-08-01", "2023-09-01", "2023-10-01", "2023-11-01", "2023-12-01", "2024-01-01", "2024-02-01", "2024-03-01"], "value": [115711.48, 86971.18, 60954.42, 88610.39, 87333.85, 87587.62, 89015.15, 103662.49, 104422.74, 104588.12, 104840.95, 105049.12, 79831.65, 79898.52, 79505.27, 44358.53, 42919.51, 42982.96]}"""
print(forecast_time_series(ts_data))