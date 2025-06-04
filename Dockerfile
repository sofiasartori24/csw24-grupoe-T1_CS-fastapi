FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY t1_cs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the app directory
COPY t1_cs/app ./app
COPY t1_cs/lambda_handler.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]