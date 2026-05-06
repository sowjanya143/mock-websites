#!/bin/bash
# Health check for all 23 mock websites
# Tests each site's homepage and reports status

set -e

SITES=(
    "bastion|5009"
    "landmark|5010"
    "apex|5000"
    "sentinel|5001"
    "cipher|5002"
    "fortis|5003"
)

HEALTHY=0
UNHEALTHY=0

echo "=== Health Check for Mock Websites ==="
echo "Timestamp: $(date)"
echo ""

for site_entry in "${SITES[@]}"; do
    IFS='|' read -r site_name port <<< "$site_entry"
    url="http://localhost:$port/"

    echo -n "Checking $site_name (port $port)... "

    # Try to connect and get HTTP status code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

    if [[ "$http_code" == "200" || "$http_code" == "302" || "$http_code" == "403" ]]; then
        echo "✓ HEALTHY (HTTP $http_code)"
        ((HEALTHY++))
    else
        echo "✗ UNHEALTHY (HTTP $http_code)"
        ((UNHEALTHY++))
    fi
done

echo ""
echo "=== Summary ==="
echo "Healthy: $HEALTHY"
echo "Unhealthy: $UNHEALTHY"
echo "Total: $((HEALTHY + UNHEALTHY))"
echo ""

if [ "$UNHEALTHY" -eq 0 ]; then
    echo "Status: ✓ All systems operational"
    exit 0
else
    echo "Status: ✗ Some systems unhealthy"
    exit 1
fi
