# Use the official Nginx image as a base
FROM nginx:latest

# Copy the Nginx configuration file (will be created in the next step)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the entrypoint script that will generate certificates
COPY entrypoint.sh /docker-entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /docker-entrypoint.sh

# Copy the startup confirmation script into the entrypoint directory
COPY confirm-startup.sh /docker-entrypoint.d/confirm-startup.sh

# Make the script executable
RUN chmod +x /docker-entrypoint.d/confirm-startup.sh

# Set the entrypoint script to run when the container starts
ENTRYPOINT ["/docker-entrypoint.sh"]

# The default command to start Nginx, which will be executed by the entrypoint script
CMD ["nginx", "-g", "daemon off;"]
