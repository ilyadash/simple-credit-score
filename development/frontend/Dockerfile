FROM python:3.10-slim

WORKDIR /app

RUN apt-get update\
    && apt-get install -y --no-install-recommends\
    build-essential\
    curl\
    git\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt\
    && pip install --no-cache-dir debugpy

COPY src src

# -------------------------------
# Expose port for streamlit running
# -------------------------------
EXPOSE 8501

# -------------------------------
# Expose port for streamlit debug
# -------------------------------
EXPOSE 5679

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# -------------------------------
# Start streamlit
# -------------------------------
#ENTRYPOINT ["tail", "-f", "/dev/null"]
#ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["python", "-m", "debugpy", \
     "--listen", "0.0.0.0:5679",\
     "--wait-for-client", \
     "-m", "streamlit", "run", "src/streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]