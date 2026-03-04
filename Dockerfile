# Production Dockerfile for FastAPI using Gunicorn with Uvicorn workers
# Choose a stable Python version (3.12 is broadly supported as of 2026)
FROM python:3.12-slim

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    GUNICORN_WORKERS=2

# Create application directory
WORKDIR /ms_app

# Install system dependencies if needed by wheels (kept minimal for slim image)
# If your project needs system libs (e.g., for database drivers), add them here.
# RUN apt-get update -qq && \
#     apt-get install -y --no-install-recommends libpq5 && \
#     rm -rf /var/lib/apt/lists/*
# psycopg2
# RUN apt-get update && apt-get install -y \
#  gcc \
#   libpq-dev \
#    python3-dev \
#     && rm -rf /var/lib/apt/lists/*
# docker build -t fastapi-app .
# docker run -it -p 8000:8000 fastapi-app
# docker logs 949e7090c492


# Upgrade pip first
RUN python -m pip install --upgrade pip

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt ./

# Install Python dependencies
# Ensure gunicorn and uvicorn are present even if not in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn "uvicorn[standard]"

# Copy the rest of the application code
COPY . .

# Create a non-root user and adjust permissions
RUN useradd -m -u 10001 -s /usr/sbin/nologin appuser && \
    chown -R appuser:appuser /ms_app
USER appuser

# Expose the application port
EXPOSE 8000

# Start the application (currently using Uvicorn). Previous Gunicorn command is kept commented below for later use.
# Tune workers via env: GUNICORN_WORKERS, PORT
# CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --workers ${GUNICORN_WORKERS} --timeout 60 --graceful-timeout 30 --keep-alive 5 --access-logfile - --error-logfile - --log-level info app.main:app"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
