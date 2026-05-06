FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Default Flask app (can be overridden via FLASK_APP env var)
ENV FLASK_APP=bastion/app.py
ENV FLASK_ENV=production
ENV PORT=5009

# Expose dynamic port (default 5009)
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Run Flask application
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 4 --worker-class sync --timeout 30 --access-logfile - --error-logfile - "${FLASK_APP%/*}.app:app"
