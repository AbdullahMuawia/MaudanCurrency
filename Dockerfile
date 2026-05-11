# Start from an official Python image
FROM python:3.14.4

# Set working directory inside the container
WORKDIR /app

# Copy dependencies first (this layer is cached — rebuilds are faster)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY backend/ .

# Expose port 8000
EXPOSE 8000

# Command to run when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]