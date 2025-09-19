#!/bin/sh

# Define paths for the certificate and key
CERT_DIR="/etc/ssl/certs"
KEY_DIR="/etc/ssl/private"
CERT_FILE="${CERT_DIR}/server.crt"
KEY_FILE="${KEY_DIR}/server.key"

# Create directories if they don't exist
mkdir -p "$CERT_DIR" "$KEY_DIR"

# Generate a self-signed certificate only if it doesn't already exist
if [ ! -f "$CERT_FILE" ]; then
  echo ">>> Generating self-signed certificate for localhost..."
  openssl req -x509 -newkey rsa:4096 -nodes \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -days 365 \
    -subj "/CN=localhost"
  echo ">>> Certificate generated."
fi

# Execute the command passed to this script (e.g., the CMD from the Dockerfile)
exec "$@"
