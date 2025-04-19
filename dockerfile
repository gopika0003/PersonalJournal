# Use official Python image
FROM python:3.13-slim

# Install system dependencies for selenium and Chrome WebDriver
RUN apt-get update \
    && apt-get install -y \
    wget \
    curl \
    unzip \
    libpq-dev gcc \
    libgtk-3-0 libdbus-1-3 libxtst6 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libnss3 libxss1 libgdk-pixbuf2.0-0 \
    && pip install --upgrade pip

# Install Google Chrome (latest version for Linux)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    || apt-get install -f -y \
    && rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver dynamically (latest version for Linux)
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

# Install webdriver-manager
RUN pip install webdriver-manager

# Install pytest and pytest-html explicitly
RUN pip install pytest==7.0.0 pytest-html==3.1.1



# Set environment variables for headless Chrome and ChromeDriver path
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome-stable
ENV CHROME_DRIVER=/usr/local/bin/chromedriver

# Set work directory
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files into the Docker container
COPY . .

# Expose default Django port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
