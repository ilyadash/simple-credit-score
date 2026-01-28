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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

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
# Copy our trained model
# -------------------------------
COPY model/ model/

# -------------------------------
# Copy application code
# -------------------------------
COPY src src

# -------------------------------
# Expose port for FASTapi app
# -------------------------------
EXPOSE 8000

# -------------------------------
# Expose port for FASTapi debug
# -------------------------------
EXPOSE 5678

# -------------------------------
# Start FastAPI (production)
# -------------------------------
ENTRYPOINT ["tail", "-f", "/dev/null"]
#CMD ["fastapi", "run", "app/src/main.py", "--port", "8000"]
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
#CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
