from openai import OpenAI

class Insights:
    def __init__(self, data, api_key):
        self.data = data
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def generate_nlp_insights(self):
        """Generate natural language insights using DeepSeek."""
        summary = self.data.describe().to_string()
        prompt = f"""
        Given the following dataset summary:
        {summary}
        Provide insights about the data, including trends, patterns, and anomalies.
        """
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        insights = response.choices[0].message.content
        
        with open("nlp_insights.txt", "w") as f:
            f.write(insights)