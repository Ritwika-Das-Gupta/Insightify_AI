import pandas as pd
import os

class DataLoader:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def load_instructions(self):
        csv_path = os.path.join(self.input_dir, "output_results.csv")
        return pd.read_csv(csv_path)

    def sample_instructions(self, n):
        df = self.load_instructions()
        return df.sample(n=n)