FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY client_a2a /app/client_a2a/

# Copy app files
COPY backend/ .

# Expose port
EXPOSE 5000

# Run Flask app
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]
