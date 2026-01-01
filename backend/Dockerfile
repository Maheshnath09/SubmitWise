FROM python:3.11-slim

WORKDIR /app

# Configure apt to be more resilient
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries

# Install system dependencies with retry logic
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements
COPY requirements-simple.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-simple.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

