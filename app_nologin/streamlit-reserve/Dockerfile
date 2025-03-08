# Streamlit Reserve Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app
COPY . .

# Expose the port
EXPOSE 8504

# Command to run the app
CMD ["streamlit", "run", "reserve_front.py"]
