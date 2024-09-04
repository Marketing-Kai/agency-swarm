from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import subprocess

class ContainerizeApplication(BaseTool):
    """
    This tool enables the agent to containerize the application using Docker.
    It provides functionalities to create Dockerfiles, build Docker images, and run Docker containers.
    """

    app_name: str = Field(
        ..., description="The name of the application to be containerized."
    )
    base_image: str = Field(
        ..., description="The base Docker image to use (e.g., python:3.8)."
    )
    requirements_file: str = Field(
        ..., description="The path to the requirements.txt file for the application."
    )
    app_directory: str = Field(
        ..., description="The directory containing the application code."
    )
    dockerfile_path: str = Field(
        ..., description="The path where the Dockerfile will be created."
    )

    def create_dockerfile(self):
        """
        Create a Dockerfile for the application.
        """
        dockerfile_content = f"""
        # Use the specified base image
        FROM {self.base_image}

        # Set the working directory
        WORKDIR /app

        # Copy the requirements file and install dependencies
        COPY {self.requirements_file} .
        RUN pip install --no-cache-dir -r {os.path.basename(self.requirements_file)}

        # Copy the application code
        COPY {self.app_directory} .

        # Specify the command to run the application
        CMD ["python", "app.py"]
        """
        with open(self.dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_content.strip())

    def build_docker_image(self):
        """
        Build the Docker image for the application.
        """
        image_name = f"{self.app_name.lower().replace(' ', '_')}_image"
        subprocess.run(["docker", "build", "-t", image_name, "-f", self.dockerfile_path, "."], check=True)
        return image_name

    def run_docker_container(self, image_name):
        """
        Run the Docker container for the application.
        """
        container_name = f"{self.app_name.lower().replace(' ', '_')}_container"
        subprocess.run(["docker", "run", "--name", container_name, "-d", image_name], check=True)
        return container_name

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method creates a Dockerfile, builds the Docker image, and runs the Docker container.
        """
        self.create_dockerfile()
        image_name = self.build_docker_image()
        container_name = self.run_docker_container(image_name)
        
        # Return a confirmation message
        return f"Application '{self.app_name}' has been containerized. Docker image '{image_name}' and container '{container_name}' have been created and started."

# Example usage:
# tool = ContainerizeApplication(
#     app_name="MyApp",
#     base_image="python:3.8",
#     requirements_file="path/to/requirements.txt",
#     app_directory="path/to/app",
#     dockerfile_path="path/to/Dockerfile"
# )
# tool.run()