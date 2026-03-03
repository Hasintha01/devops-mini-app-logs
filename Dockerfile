FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables for S3 logging (can be overridden at runtime)
ENV S3_BUCKET_NAME=devops-mini-app-logs
ENV AWS_REGION=us-east-1
ENV ENABLE_S3_LOGGING=false

EXPOSE 5000

CMD ["python", "app.py"]
