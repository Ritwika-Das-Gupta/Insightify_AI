import pandas as pd
import sweetviz as sv
import os

class EDA:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.data = None

    def load_data(self):
        """Load the CSV file into a pandas DataFrame."""
        try:
            self.data = pd.read_csv(self.input_file)
            return self.data
        except Exception as e:
            print(f"Error loading file: {e}")
            return None

    def perform_eda(self):
        """Perform automated EDA using Sweetviz."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate EDA report
        report = sv.analyze(self.data)
        report.show_html(os.path.join(self.output_dir, "automated_eda_report.html"))