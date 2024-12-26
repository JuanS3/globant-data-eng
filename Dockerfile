FROM python:3.12-slim

WORKDIR /app

# Install system dependencies BEFORE copying your application code
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client libpq-dev gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]