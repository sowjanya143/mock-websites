"""Honeypot detection - catch bots filling hidden fields."""

import uuid


def generate_honeypot_field_name():
    """Generate a unique honeypot field name."""
    return f'hf_{uuid.uuid4().hex[:12]}'


def is_honeypot_filled(form_data, field_name):
    """Check if honeypot field has been filled (indicates bot)."""
    return field_name in form_data and form_data[field_name].strip() != ''


def inject_honeypot_fields(session):
    """Generate honeypot fields to inject into forms."""
    honeypot_field = generate_honeypot_field_name()
    session['honeypot_field'] = honeypot_field
    return {
        'field_name': honeypot_field,
        'display_name': 'Website',  # Misleading label
    }


def validate_form_submission(form_data, session):
    """Validate form - return False if honeypot filled (bot detected)."""
    honeypot_field = session.get('honeypot_field')

    if not honeypot_field:
        return True

    # If honeypot field is filled, it's a bot
    if is_honeypot_filled(form_data, honeypot_field):
        return False

    return True
