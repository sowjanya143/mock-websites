#!/bin/bash
# Backup all mock website data
# Creates a timestamped archive of all data directories

set -e

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="./backups"
BACKUP_FILE="$BACKUP_DIR/mock-websites-backup-$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "=== Backup Script for Mock Websites ==="
echo "Timestamp: $TIMESTAMP"
echo "Backup destination: $BACKUP_FILE"
echo ""

# Directories to backup
DIRS_TO_BACKUP=(
    "bastion/data"
    "landmark/data"
    "apex/data"
    "sentinel/data"
    "cipher/data"
    "fortis/data"
    ".env.production"
)

echo "Files to backup:"
for dir in "${DIRS_TO_BACKUP[@]}"; do
    if [ -e "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  - $dir (not found, skipping)"
    fi
done

echo ""
echo "Creating backup archive..."

# Create backup archive
tar -czf "$BACKUP_FILE" \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude=".git" \
    --exclude=".env.local" \
    "${DIRS_TO_BACKUP[@]}" 2>/dev/null || true

if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✓ Backup created successfully"
    echo "  File: $(basename $BACKUP_FILE)"
    echo "  Size: $SIZE"
    echo ""

    # Keep only last 7 backups
    echo "Cleaning up old backups (keeping last 7)..."
    cd "$BACKUP_DIR"
    ls -t mock-websites-backup-*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null || true
    cd - > /dev/null

    echo "Remaining backups:"
    ls -lh "$BACKUP_DIR"/mock-websites-backup-*.tar.gz 2>/dev/null | awk '{print "  " $NF}' || echo "  None"
    echo ""
    echo "=== Backup Complete ==="
else
    echo "✗ Backup creation failed"
    exit 1
fi
