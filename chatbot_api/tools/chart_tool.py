# chart_tool.py
import numpy as np

class ChartTool:
    def generate_chart_data(self, user_input):
        # Extract data from user input (dummy data for example)
        data = self.extract_data(user_input)
        return {
            "chart_data": {
                "x": data["x"].tolist(),
                "col1": data["col1"].tolist(),
                "col2": data["col2"].tolist(),
                "col3": data["col3"].tolist()
            }
        }

    def extract_data(self, user_input):
        # Example data extraction logic (you can replace this with actual logic)
        return {
            "x": np.arange(10),
            "col1": np.random.randn(10),
            "col2": np.random.randn(10),
            "col3": np.random.randn(10)
        }