# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends\
    build-essential\
    curl\
    git\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

COPY src src

ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]