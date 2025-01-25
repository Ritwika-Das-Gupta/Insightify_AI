import argparse
from automl_eda import EDA, Visualization, Report

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Automated EDA and Visualization Tool")
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, required=True, help="Path to the output directory")
    args = parser.parse_args()

    # Specify input file and output directory from command line
    input_file = args.input
    output_dir = args.output

    # Define the visualizations directory directly in the main script
    visualizations = "./visualizations"  # Replace with your actual path

    # Load data
    eda = EDA(input_file, output_dir)
    data = eda.load_data()

    # Perform EDA
    eda.perform_eda()

    # Generate visualizations and insights using DeepSeek
    api_key = "api_key"
    visualization = Visualization(data, api_key, visualizations)  # Pass the variable
    visualization.create_visualizations_and_insights()

    # Generate the final PDF report
    report = Report(data, output_dir, visualizations)  # Pass the variable
    report.generate_report()

if __name__ == "__main__":
    main()