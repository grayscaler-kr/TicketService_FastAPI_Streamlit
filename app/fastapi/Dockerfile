# FastAPI Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "fastapi-app.main:app", "--host", "0.0.0.0", "--port", "8000"]
