#!/usr/bin/with-contenv bashio

bashio::log.info "Starting Shelly HA Manager..."

# Get version from config.yaml
export ADDON_VERSION=$(bashio::addon.version)

# Get configuration
export ADMIN_PASSWORD=$(bashio::config 'admin_password')

# Log configuration (without showing password)
if bashio::var.has_value "${ADMIN_PASSWORD}"; then
    bashio::log.info "Admin password configured"
else
    bashio::log.warning "No admin password set - limited functionality"
fi

# Set port for ingress
export INGRESS_PORT=8099
export PORT=8099

bashio::log.info "Fetching Shelly devices from Home Assistant..."

# Start the Flask application
cd /app
exec python3 -u app.py
