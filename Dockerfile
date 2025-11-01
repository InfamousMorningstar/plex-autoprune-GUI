FROM python:3.11-slim

# Set UTF-8 encoding for Python and system
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY daemon.py .
COPY web.py .
COPY main.py .
COPY templates/ templates/
COPY static/ static/

# Create state directory
RUN mkdir -p /app/state

# Expose web UI port
EXPOSE 8080

# Run the combined application
CMD ["python", "main.py"]
