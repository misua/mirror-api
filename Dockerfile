# Multi-stage build to keep image size down
FROM python:3.11-slim as builder

WORKDIR /build

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final image
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Run on port 4004 as required
EXPOSE 4004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4004"]
