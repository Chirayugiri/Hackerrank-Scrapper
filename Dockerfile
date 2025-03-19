# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (new method)
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Verify Chrome installation
RUN google-chrome --version

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["python", "main.py"]
