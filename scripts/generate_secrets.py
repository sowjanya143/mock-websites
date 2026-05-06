#!/usr/bin/env python3
"""Generate secure secret keys for all 23 mock websites."""

import secrets
import os
from pathlib import Path

def generate_secret(length=32):
    """Generate a secure random secret key."""
    return secrets.token_urlsafe(length)

def main():
    sites = [
        'BASTION',
        'LANDMARK',
        'APEX',
        'SENTINEL',
        'CIPHER',
        'FORTIS',
        'SITE_5004',
        'SITE_5005',
        'SITE_5006',
        'SITE_5007',
        'SITE_5008',
    ]

    env_file = Path('.env.production')

    print("Generating secure secret keys for all sites...")
    print("=" * 60)

    secrets_dict = {}
    for site in sites:
        secret = generate_secret(48)
        secrets_dict[site] = secret
        print(f"{site}_SECRET_KEY={secret}")

    print("=" * 60)
    print()

    # Write to .env.production if it exists
    if env_file.exists():
        print(f"Updating {env_file}...")
        with open(env_file, 'r') as f:
            content = f.read()

        # Replace existing keys
        for site, secret in secrets_dict.items():
            key_name = f"{site}_SECRET_KEY"
            # Replace pattern: KEY_NAME=old_value
            import re
            pattern = f"{key_name}=.*"
            content = re.sub(pattern, f"{key_name}={secret}", content)

        with open(env_file, 'w') as f:
            f.write(content)

        print(f"✓ Updated {env_file}")
    else:
        print(f"⚠ File {env_file} not found. Please create it manually.")
        print()
        print("Create .env.production with the secrets above.")

    print()
    print("=== Secret Generation Complete ===")
    print(f"Generated {len(secrets_dict)} secure secret keys")
    print("Store these safely and never commit to git!")
    print()
    print("Add to .gitignore:")
    print("  .env.production")
    print("  .env.local")
    print("  ssl/")

if __name__ == '__main__':
    main()
