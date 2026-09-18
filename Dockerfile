FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Install runtime dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY service/ ./service/

# Run as a non-root user. Group is set to root (GID 0) and made writable
# by the group, since OpenShift runs containers under an arbitrary UID
# that always belongs to GID 0 -- this lets Flask create its instance/
# folder (for the default SQLite file) regardless of the runtime UID.
RUN useradd --uid 1000 flask-user && \
    chown -R flask-user:0 /app && \
    chmod -R g=u /app
USER flask-user

ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["gunicorn"]
CMD ["--bind=0.0.0.0:8080", "--log-level=info", "service:app"]
