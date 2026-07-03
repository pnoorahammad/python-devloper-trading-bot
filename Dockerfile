FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create logs directory
RUN mkdir -p /app/logs

# Expose port for FastAPI
EXPOSE 8000

# Default: start the FastAPI server
# Override with: docker run ... python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
