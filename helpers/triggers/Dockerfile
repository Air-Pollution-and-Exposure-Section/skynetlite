# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the entire project directory into the container
COPY . .

# Install the project in editable mode
RUN pip install -e .

# Define the command to run your script
CMD ["python", "helpers/triggers/trigger_temperature_table_triggers.py"]

