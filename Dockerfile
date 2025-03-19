# Use official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl xvfb libxi6 libgconf-2-4 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome manually
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]
