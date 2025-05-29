FROM nginx:alpine

# Copy the application files to the nginx html directory
COPY . /usr/share/nginx/html/

# Copy a custom nginx configuration if needed
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]