FROM python:3.11-slim

# Copy app files
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY src /app/src
COPY scripts /app/scripts

# Set PYTHONPATH to project root
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "src/etl_pipeline/main.py"]