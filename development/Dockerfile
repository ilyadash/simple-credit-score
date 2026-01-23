# -------------------------------
# Base image
# -------------------------------
FROM python:3.10-slim

# -------------------------------
# Environment variables
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1

# -------------------------------
# System dependencies
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Set workdir
# -------------------------------
WORKDIR /app

# -------------------------------
# Install Python dependencies
# -------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Copy application code
# -------------------------------
COPY app/ app/
COPY model/ model/

# -------------------------------
# Expose port
# -------------------------------
EXPOSE 8009

# -------------------------------
# Start FastAPI (production)
# -------------------------------
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8009", "--workers", "2"]
