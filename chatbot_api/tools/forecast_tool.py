from prophet import Prophet
from datetime import datetime
import pandas as pd
import json

def forecast_time_series(data: str) -> str:
    try:
        # Load the data
        df = pd.read_json(data)
        
        # Prepare the data for Prophet
        df.rename(columns={"date": "ds", "value": "y"}, inplace=True)
        
        # Fit the model
        model = Prophet()
        model.fit(df)
        
        # Make a future dataframe for predictions
        future = model.make_future_dataframe(periods=30)  # Forecast for next 30 days
        forecast = model.predict(future)
        
        # Prepare the output
        forecast_output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
        # return forecast_output
        return forecast_output.to_json(orient="records")
    
    except Exception as e:
        return json.dumps({"error": str(e)})
