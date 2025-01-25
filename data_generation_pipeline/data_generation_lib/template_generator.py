class TemplateGenerator:
    def __init__(self, template_file):
        self.template_file = template_file

    def load_template(self):
        """Load the template from the file."""
        with open(self.template_file, "r") as file:
            return file.read()