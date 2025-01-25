from fpdf import FPDF
import os

class Report:
    def __init__(self, data, output_dir, visualizations):
        self.data = data
        self.output_dir = output_dir
        self.visualizations = visualizations # Use the variable passed from the main script

    def generate_report(self):
        """Generate a PDF report with visualizations and insights."""
        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add dataset summary
        pdf.cell(200, 10, txt="Automated EDA Report", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt="Dataset Summary", ln=True, align="L")
        pdf.ln(5)
        summary = f"""
        Number of Rows: {self.data.shape[0]}
        Number of Columns: {self.data.shape[1]}
        Missing Values: {self.data.isnull().sum().sum()}
        Numerical Columns: {list(self.data.select_dtypes(include=['float64', 'int64']).columns)}
        Categorical Columns: {list(self.data.select_dtypes(include=['object']).columns)}
        """
        pdf.multi_cell(0, 10, txt=summary)
        pdf.ln(10)

        # Add visualization insights
        pdf.cell(200, 10, txt="Visualization Insights", ln=True, align="L")
        pdf.ln(5)
        insights_path = os.path.join(self.visualizations, "visualization_insights.txt")
        if os.path.exists(insights_path):
            with open(insights_path, "r") as f:
                insights = f.read()
            pdf.multi_cell(0, 10, txt=insights)
        else:
            pdf.multi_cell(0, 10, txt="No visualization insights found.")
        pdf.ln(10)

        # Add visualizations
        pdf.cell(200, 10, txt="Visualizations", ln=True, align="L")
        pdf.ln(5)

        # Check if visualizations directory exists
        if os.path.exists(self.visualizations):
            # Add all generated images
            for file in os.listdir(self.visualizations):
                if file.endswith(".png"):
                    # Debug: Print the file path
                    print(f"Adding image: {file}")
                    
                    # Add image to PDF
                    pdf.cell(200, 10, txt=file, ln=True, align="L")
                    pdf.image(os.path.join(self.visualizations, file), x=10, y=None, w=180)
                    pdf.ln(10)
        else:
            pdf.multi_cell(0, 10, txt="No visualizations found.")

        # Save the PDF in the output directory
        pdf_output_path = os.path.join(self.output_dir, "final_automated_eda_report.pdf")
        pdf.output(pdf_output_path)
        print(f"PDF report saved to: {pdf_output_path}")