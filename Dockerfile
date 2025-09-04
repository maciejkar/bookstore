# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY ./app /app/app
COPY ./tests /app/tests

# Create logs directory
RUN mkdir -p /app/logs

# Expose port and define volume for logs
EXPOSE 8000
VOLUME /app/logs

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
