FROM python:3.11-slim

LABEL maintainer="TheCloudloop - pgvector working example"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    curl software-properties-common \
    && rm -rf /var/lib/apt/lists/*
 
WORKDIR /app

COPY requirements.txt app.py generate_embeddings.py ./

RUN pip3 install -r requirements.txt

EXPOSE 8501

CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0

