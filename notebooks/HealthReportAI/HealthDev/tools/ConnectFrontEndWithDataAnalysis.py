from agency_swarm.tools import BaseTool
from pydantic import Field
import streamlit as st
import pandas as pd
import json

class ConnectFrontEndWithDataAnalysis(BaseTool):
    """
    This tool enables the agent to connect the front-end web UI with data analyses performed in Jupyter Notebooks.
    It provides functionalities to fetch data from Jupyter Notebooks and display it on the web UI.
    It handles different data formats like CSV, JSON, and Pandas DataFrames.
    """

    data_source: str = Field(
        ..., description="The path to the data source file (CSV, JSON) or a serialized Pandas DataFrame."
    )
    data_format: str = Field(
        ..., description="The format of the data source (csv, json, dataframe)."
    )

    def read_data(self):
        """
        Read data from the specified data source.
        """
        if self.data_format == 'csv':
            data = pd.read_csv(self.data_source)
        elif self.data_format == 'json':
            with open(self.data_source, 'r') as file:
                data = json.load(file)
            data = pd.json_normalize(data)
        elif self.data_format == 'dataframe':
            data = pd.read_pickle(self.data_source)
        else:
            raise ValueError("Unsupported data format. Please use 'csv', 'json', or 'dataframe'.")
        return data

    def process_data(self, data):
        """
        Process the data if necessary. This method can be customized for specific data processing needs.
        """
        # Example processing: Convert all column names to uppercase
        data.columns = [col.upper() for col in data.columns]
        return data

    def render_data(self, data):
        """
        Render the data on the web UI using Streamlit.
        """
        st.dataframe(data)

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method reads data from Jupyter Notebooks, processes it if necessary, and renders it on the web UI.
        """
        data = self.read_data()
        processed_data = self.process_data(data)
        self.render_data(processed_data)
        
        # Return a confirmation message
        return "Data has been fetched from Jupyter Notebooks and rendered on the web UI."

# Example usage:
# tool = ConnectFrontEndWithDataAnalysis(
#     data_source="path/to/data.csv",
#     data_format="csv"
# )
# tool.run()