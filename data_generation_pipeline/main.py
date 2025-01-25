import argparse
# from data_generation_lib.pipeline import DataGenerationPipeline
from data_generation_lib import DataLoader, DataGenerationPipeline

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run the data generation pipeline.")
    
    # Required arguments
    parser.add_argument("template_file", type=str, help="Path to the template file (e.g., template.txt).")
    parser.add_argument("input_dir", type=str, help="Path to the input directory containing output_results.csv.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory for generated data.")
    parser.add_argument("language", type=str, help="Language for the generated conversations (e.g., 'English', 'Spanish').")
    
    # Optional arguments with default values
    parser.add_argument("--n", type=int, default=5, help="Number of instructions to process at a time (default: 5).")
    parser.add_argument("--iterations", type=int, default=15, help="Number of iterations to run (default: 15).")
    
    # Parse arguments
    args = parser.parse_args()

    # Initialize and run the pipeline
    pipeline = DataGenerationPipeline(args.template_file, args.input_dir, args.output_dir, args.language)
    pipeline.run(n=args.n, iterations=args.iterations)

if __name__ == "__main__":
    main()