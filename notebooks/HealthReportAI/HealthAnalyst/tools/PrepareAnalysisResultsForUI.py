from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os

class PrepareAnalysisResultsForUI(BaseTool):
    """
    This tool enables the agent to prepare the results of data analyses for integration into the user interface.
    It provides functionalities to format the results, create visualizations, and export the data in a suitable format for the UI.
    """

    analysis_results: dict = Field(
        ..., description="The dictionary containing the analysis results."
    )
    output_directory: str = Field(
        ..., description="The directory where the formatted results and visualizations will be saved."
    )

    def format_results(self):
        """
        Format the analysis results for UI integration.
        """
        formatted_results = json.dumps(self.analysis_results, indent=4)
        with open(os.path.join(self.output_directory, 'formatted_results.json'), 'w') as f:
            f.write(formatted_results)
        return formatted_results

    def create_visualizations(self):
        """
        Create visualizations from the analysis results.
        """
        sns.set(style="whitegrid")
        for key, value in self.analysis_results.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        plt.figure(figsize=(10, 6))
                        sns.barplot(x=[sub_key], y=[sub_value])
                        plt.title(f'{key} - {sub_key}')
                        plt.savefig(os.path.join(self.output_directory, f'{key}_{sub_key}.png'))
                        plt.close()
            elif isinstance(value, (int, float)):
                plt.figure(figsize=(10, 6))
                sns.barplot(x=[key], y=[value])
                plt.title(key)
                plt.savefig(os.path.join(self.output_directory, f'{key}.png'))
                plt.close()

    def export_data(self):
        """
        Export the analysis results in CSV format for UI integration.
        """
        df = pd.DataFrame(self.analysis_results)
        df.to_csv(os.path.join(self.output_directory, 'analysis_results.csv'), index=False)

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method formats the analysis results, creates visualizations, and exports the data for UI integration.
        """
        formatted_results = self.format_results()
        self.create_visualizations()
        self.export_data()
        
        # Return a confirmation message
        return "Analysis results have been prepared for UI integration. Formatted results, visualizations, and exported data have been saved."

# Example usage:
# tool = PrepareAnalysisResultsForUI(
#     analysis_results={
#         "mean_age": 35.5,
#         "median_income": 55000,
#         "std_dev_bmi": 4.2,
#         "insights": {
#             "age": {"mean": 35.5, "median": 34, "std_dev": 5.1},
#             "income": {"mean": 55000, "median": 54000, "std_dev": 12000}
#         }
#     },
#     output_directory="path/to/output"
# )
# tool.run()