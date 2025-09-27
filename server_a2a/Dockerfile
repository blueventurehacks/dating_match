FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY server_a2a/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server_a2a code
COPY server_a2a/ ./server_a2a/
COPY agents/ ./agents/

# Expose ports for both agents
EXPOSE 9996 9997

# Set environment variable for Docker detection
ENV RUNNING_IN_DOCKER=true

CMD ["python", "-m", "server_a2a.main"]