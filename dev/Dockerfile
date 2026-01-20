FROM python:3.10-slim

WORKDIR /app

COPY ai/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai/ ai/
COPY logs/ logs/

CMD ["python", "ai/anomaly_detector.py"]
