FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Install runtime dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY service/ ./service/

# Run as a non-root user
RUN useradd --uid 1000 flask-user && chown -R flask-user:flask-user /app
USER flask-user

ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["gunicorn"]
CMD ["--bind=0.0.0.0:8080", "--log-level=info", "service:app"]
