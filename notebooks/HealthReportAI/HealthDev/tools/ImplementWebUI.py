from agency_swarm.tools import BaseTool
from pydantic import Field
import streamlit as st
import os

class ImplementWebUI(BaseTool):
    """
    This tool enables the agent to implement a web user interface (UI) using frameworks like Streamlit.
    It provides functionalities to create, update, and render web pages with basic UI elements like text, images, and forms.
    """

    page_title: str = Field(
        ..., description="The title of the web page."
    )
    page_content: str = Field(
        ..., description="The content to be displayed on the web page."
    )
    image_url: str = Field(
        None, description="The URL of the image to be displayed on the web page."
    )
    form_data: dict = Field(
        None, description="A dictionary containing form data to be displayed on the web page."
    )

    def set_page_title(self):
        """
        Set the title of the web page.
        """
        st.title(self.page_title)

    def add_content(self):
        """
        Add content to the web page.
        """
        st.write(self.page_content)

    def add_image(self):
        """
        Add an image to the web page if the image URL is provided.
        """
        if self.image_url:
            st.image(self.image_url)

    def add_form(self):
        """
        Add a form to the web page if form data is provided.
        """
        if self.form_data:
            with st.form(key='my_form'):
                for field, value in self.form_data.items():
                    st.text_input(label=field, value=value)
                submit_button = st.form_submit_button(label='Submit')

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method uses Streamlit to create, update, and render web pages with basic UI elements.
        """
        self.set_page_title()
        self.add_content()
        self.add_image()
        self.add_form()
        
        # Return a confirmation message
        return f"Web page '{self.page_title}' has been rendered with the provided content."

# Example usage:
# tool = ImplementWebUI(
#     page_title="My Web Page",
#     page_content="Welcome to my web page!",
#     image_url="https://example.com/image.png",
#     form_data={"Name": "Enter your name", "Email": "Enter your email"}
# )
# tool.run()