import pandas as pd
from datetime import datetime
import os

class DataSaver:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_data(self, data):
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.output_dir, f"{current_datetime}.csv")
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to: {filename}")