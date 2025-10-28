#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create/recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
NGINX_CONF="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static/" "$NGINX_CONF"; then
    sudo sed -i '/listen 80 default_server;/a \
    \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' "$NGINX_CONF"
fi

# Restart Nginx
sudo service nginx restart

exit 0
