from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class PerformDataAnalysis(BaseTool):
    """
    This tool enables the agent to perform data analysis and interpretation on health data.
    It provides functionalities to load data, perform statistical analyses, and generate insights.
    """

    data_source: str = Field(
        ..., description="The path to the health data file (CSV or Excel)."
    )
    data_format: str = Field(
        ..., description="The format of the data source (csv or excel)."
    )
    output_directory: str = Field(
        ..., description="The directory where the analysis results and plots will be saved."
    )

    def load_data(self):
        """
        Load data from the specified data source.
        """
        if self.data_format == 'csv':
            data = pd.read_csv(self.data_source)
        elif self.data_format == 'excel':
            data = pd.read_excel(self.data_source)
        else:
            raise ValueError("Unsupported data format. Please use 'csv' or 'excel'.")
        return data

    def perform_statistical_analysis(self, data):
        """
        Perform basic statistical analysis on the data.
        """
        description = data.describe()
        correlation_matrix = data.corr()
        return description, correlation_matrix

    def generate_insights(self, data):
        """
        Generate insights from the data.
        """
        insights = {}
        for column in data.select_dtypes(include=[np.number]).columns:
            insights[column] = {
                'mean': data[column].mean(),
                'median': data[column].median(),
                'std_dev': data[column].std(),
                'variance': data[column].var()
            }
        return insights

    def plot_data(self, data):
        """
        Generate and save plots for the data.
        """
        sns.set(style="whitegrid")
        for column in data.select_dtypes(include=[np.number]).columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(data[column], kde=True)
            plt.title(f'Distribution of {column}')
            plt.savefig(os.path.join(self.output_directory, f'{column}_distribution.png'))
            plt.close()

        plt.figure(figsize=(10, 6))
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig(os.path.join(self.output_directory, 'correlation_matrix.png'))
        plt.close()

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method loads data, performs statistical analyses, generates insights, and saves plots.
        """
        data = self.load_data()
        description, correlation_matrix = self.perform_statistical_analysis(data)
        insights = self.generate_insights(data)
        self.plot_data(data)
        
        # Save the statistical analysis results
        description.to_csv(os.path.join(self.output_directory, 'data_description.csv'))
        correlation_matrix.to_csv(os.path.join(self.output_directory, 'correlation_matrix.csv'))
        
        # Save the insights
        with open(os.path.join(self.output_directory, 'insights.txt'), 'w') as f:
            for column, stats in insights.items():
                f.write(f"{column}:\n")
                for stat, value in stats.items():
                    f.write(f"  {stat}: {value}\n")
                f.write("\n")
        
        # Return a confirmation message
        return "Data analysis and interpretation have been completed. Results and plots have been saved."

# Example usage:
# tool = PerformDataAnalysis(
#     data_source="path/to/health_data.csv",
#     data_format="csv",
#     output_directory="path/to/output"
# )
# tool.run()