import re
import json
from data_generation_lib import DataLoader, TemplateGenerator,TextGenerator, DataSaver
# from data_generation_lib.template_generator import TemplateGenerator
# from data_generation_lib.text_generator import TextGenerator
# from data_generation_lib.data_saver import DataSaver

class DataGenerationPipeline:
    def __init__(self, template_file, input_dir, output_dir, language):
        self.template_generator = TemplateGenerator(template_file)
        self.data_loader = DataLoader(input_dir)
        self.data_saver = DataSaver(output_dir)
        self.language = language  # Store the language

    def run(self, n, iterations=15):
        global_data = []
        for i in range(iterations):
            selected_rows = self.data_loader.sample_instructions(n)
            input_data = self._prepare_input_data(selected_rows)
            
            # Load the template
            template = self.template_generator.load_template()
            
            # Initialize TextGenerator with the loaded template
            text_generator = TextGenerator(template)
            
            # Generate conversations
            result = text_generator.generate_conversations(input_data)
            processed_data = self._process_results(result, selected_rows)
            global_data.extend(processed_data)
            print(f"Iteration {i + 1}/{iterations} complete.")
        
        # Save the generated data
        self.data_saver.save_data(global_data)

    def _prepare_input_data(self, selected_rows):
        input_data = []
        for _, row in selected_rows.iterrows():
            input_data.append({
                "examples": row['EXAMPLE'],
                "system_prompt": (
                    "You are an AI assistant that generates multi-turn conversations between a user and an assistant. "
                    "These conversations are natural and human-like. Each conversation should have user and assistant tags "
                    "in a single turn; no consecutive user-user, assistant-assistant, or assistant-user tags are allowed. "
                    f"Given examples for the type of conversations that should be generated in given format for {row['DOMAIN']} domain in {row['SECTOR']} sector and for {row['TOPIC']}. "
                    f"Generate the conversations in {self.language} language."  # Include the language in the system prompt
                ),
                "instruction_id": row['ID']
            })
        return input_data

    def _process_results(self, result, selected_rows):
        global_data = []
        for idx, res in enumerate(result):
            result_string = res["generation"]
            example_pattern = r"<EXAMPLE>\s*(\[[^\]]+\])\s*</EXAMPLE>"
            examples = re.findall(example_pattern, result_string, re.DOTALL)
            for example_text in examples:
                try:
                    json_text = example_text.replace("'", '"')
                    conversation = json.loads(json_text)
                    turns = len(conversation) // 2
                    global_data.append({
                        "Messages": conversation,
                        "Turns": turns,
                        "Domain": selected_rows.iloc[idx]['DOMAIN'],
                        "Sector": selected_rows.iloc[idx]['SECTOR'],
                        "Topic": selected_rows.iloc[idx]['TOPIC'],
                        "User_Gender": selected_rows.iloc[idx]['USER'],
                        "Assistant_Gender": selected_rows.iloc[idx]['ASSISTANT'],
                        "Instruction_ID": selected_rows.iloc[idx]['ID'],
                        "Language": self.language  # Include the language in the output data
                    })
                except json.JSONDecodeError as e:
                    print(f"Failed to parse conversation example: {e}. Raw data:\n{example_text}")
                    continue
        return global_data