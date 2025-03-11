# Use Python base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Ollama inside the container
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set correct permissions for start.sh
RUN chmod +x start.sh

# Run Alembic migrations
RUN alembic upgrade head

# Start Ollama and FastAPI
CMD ["/bin/bash", "start.sh"]
