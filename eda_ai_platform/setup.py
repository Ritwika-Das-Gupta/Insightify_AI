from setuptools import setup, find_packages

setup(
    name="automl_eda",
    version="0.1.0",
    description="A Python library for automated EDA and insights generation.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "sweetviz",
        "seaborn",
        "matplotlib",
        "scikit-learn",
        "jinja2",
        "deepseek"  # Hypothetical DeepSeek API
    ],
    python_requires=">=3.6",
)