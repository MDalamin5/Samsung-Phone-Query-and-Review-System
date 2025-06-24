FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend code + env + requirements
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI
CMD ["python", "main.py"]
