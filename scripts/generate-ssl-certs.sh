#!/bin/bash
# Generate self-signed SSL certificates for all 23 mock websites
# For production, use Let's Encrypt or your organization's CA

set -e

SSL_DIR="./ssl"
DAYS_VALID=365

mkdir -p "$SSL_DIR"

echo "Generating SSL certificates for 23 mock websites..."

# Function to generate certificate
generate_cert() {
    local site_name=$1
    local domain=$2

    echo "Generating certificate for $site_name ($domain)..."

    openssl req -x509 -newkey rsa:4096 \
        -keyout "$SSL_DIR/${site_name}.key" \
        -out "$SSL_DIR/${site_name}.crt" \
        -days "$DAYS_VALID" \
        -nodes \
        -subj "/C=US/ST=NY/L=New York/O=Mock Company/CN=$domain"

    echo "✓ Created $SSL_DIR/${site_name}.{crt,key}"
}

# Generate certificates for all sites
generate_cert "bastion" "bastion.local"
generate_cert "landmark" "landmark.local"
generate_cert "apex" "apex.local"
generate_cert "sentinel" "sentinel.local"
generate_cert "cipher" "cipher.local"
generate_cert "fortis" "fortis.local"

# Generate placeholder certs for remaining 17 sites
for i in {4..8}; do
    generate_cert "site-500$i" "site-500$i.local"
done

# Create wildcard certificate
echo "Generating wildcard certificate..."
openssl req -x509 -newkey rsa:4096 \
    -keyout "$SSL_DIR/wildcard.key" \
    -out "$SSL_DIR/wildcard.crt" \
    -days "$DAYS_VALID" \
    -nodes \
    -subj "/C=US/ST=NY/L=New York/O=Mock Company/CN=*.local"

echo "✓ Created $SSL_DIR/wildcard.{crt,key}"

# Set proper permissions
chmod 600 "$SSL_DIR"/*.key
chmod 644 "$SSL_DIR"/*.crt

echo ""
echo "=== SSL Certificate Generation Complete ==="
echo "Location: $SSL_DIR/"
echo "Valid for: $DAYS_VALID days"
echo ""
echo "Files created:"
ls -lh "$SSL_DIR"/*.crt "$SSL_DIR"/*.key 2>/dev/null | awk '{print "  " $NF}'
echo ""
echo "NOTE: These are self-signed certificates for development/testing."
echo "For production, use Let's Encrypt (certbot) or your organization's CA."
echo ""
echo "Example Let's Encrypt setup:"
echo "  sudo certbot certonly --standalone -d bastion.yourdomain.com"
echo "  sudo certbot certonly --standalone -d landmark.yourdomain.com"
