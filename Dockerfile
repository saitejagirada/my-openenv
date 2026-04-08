# Use lightweight python image
FROM python:3.10-slim

# Set strict limits awareness
ENV PYTHONUNBUFFERED=1
ENV API_BASE_URL="https://api.openai.com/v1"
ENV MODEL_NAME="gpt-4.1-mini"
ENV ENABLE_WEB_INTERFACE=true

# Setup working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install dependencies securely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all core files
COPY . /app

# Ensure HF Space port exposes correctly
EXPOSE 7860

# Alternative CMD for testing locally:
# CMD ["python", "inference.py"]

# CMD strictly runs the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]