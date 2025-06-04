FROM python:3.9-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY t1_cs/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root user
RUN addgroup --system app && \
    adduser --system --group app && \
    chown -R app:app /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY t1_cs/app ./app
COPY t1_cs/lambda_handler.py .

# Set permissions
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the port the app runs on
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]