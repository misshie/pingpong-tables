#!/bin/sh
set -e

# Add a small delay to ensure logs appear after other startup messages.
sleep 1

echo "==========================================================="
echo " API service is healthy. Nginx is starting."
echo " "
echo " Application should now be ready at: https://localhost"
echo "==========================================================="

# This script will exit, and the main Nginx entrypoint will continue.
