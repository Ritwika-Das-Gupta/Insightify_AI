import os
from openai import OpenAI

class Visualization:
    def __init__(self, data, api_key, visualizations):
        self.data = data
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.visualizations= visualizations  # Use the variable passed from the main script

    def _get_data_summary(self):
        """Generate a summary of the dataset for DeepSeek."""
        summary = {
            "columns": list(self.data.columns),
            "data_types": self.data.dtypes.to_dict(),
            "sample_data": self.data.head().to_dict()
        }
        return summary

    def _generate_visualization_code_and_insights(self):
        """Ask DeepSeek to generate visualization code and insights."""
        summary = self._get_data_summary()
        prompt = f"""
        You are a data visualization expert. Given the following dataset summary:
        {summary}
        Please analyze the dataset and create meaningful visualizations and provide their images along with insights from those visualizations.
        The code should:
        1. Save each plot as an image file in the directory specified by `visualizations`.
        2. You have to analyze the given data based on your intelligence to generate 6 to 7 plots.
        Give proper explanation of each plot.
        3. Give bar chart, pie chart, donut chart, heatmep, scatterplot, timesiries plot, box plot and many more that suits the data
        Return the Python code for visualizations and the explanations for each plot in the following format:
        ```python
        # Visualization Code
        <code>
        ```

        ```text
        # Insights
        <insights>
        ```
        """
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        return response.choices[0].message.content

    def create_visualizations_and_insights(self):
        """Generate visualizations and insights using DeepSeek."""
        response = self._generate_visualization_code_and_insights()
        try:
            # Extract code and insights from the response
            code = response.split("```python")[1].split("```")[0].strip()
            insights = response.split("```text")[1].split("```")[0].strip()

            # Ensure the visualizations directory exists
            os.makedirs(self.visualizations, exist_ok=True)

            # Execute the generated code
            exec(code, {"visualizations": self.visualizations})

            # Save insights to a file in the visualizations directory
            with open(os.path.join(self.visualizations, "visualization_insights.txt"), "w") as f:
                f.write(insights)

            print("Visualizations and insights generated successfully!")
        except Exception as e:
            print(f"Error executing visualization code: {e}")
