from distilabel.steps.tasks import TextGeneration
from distilabel.llms import OpenAILLM

class TextGenerator:
    def __init__(self, template):
        self.template = template

    def initialize_text_gen(self):
        return TextGeneration(
            llm=OpenAILLM(
                model="deepseek-chat",
                base_url=r"https://api.deepseek.com",
                api_key="sk-4d4ee46ae243411d8efc9f8dd91961c9",
                generation_kwargs={
                    'max_new_tokens': 5000
                }
            ),
            template=self.template,
            columns=["examples", "instruction_id"],
        )

    def generate_conversations(self, input_data):
        text_gen = self.initialize_text_gen()
        text_gen.load()
        return next(text_gen.process(input_data))