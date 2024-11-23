# Start with an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data required for processing
# RUN python -m nltk.downloader punkt

# Copy the rest of the application code
COPY . .

# Ensure the ollama models are installed if not already present
RUN mkdir -p /app/models

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Start the server script by default
CMD ["/entrypoint.sh"]
