"""Popup rendering and management utilities."""

import random

from flask import session


def render_popup(popup_type='newsletter', auto_dismiss=False, dismiss_delay=5000):
    """
    Return popup data dictionary with title, content, and button.

    Stores popup state in session.

    Args:
        popup_type (str): Type of popup ('newsletter', 'alert', 'survey')
        auto_dismiss (bool): Whether popup should auto-dismiss
        dismiss_delay (int): Milliseconds before auto-dismiss

    Returns:
        dict: Popup data with keys: type, title, content, button, auto_dismiss, dismiss_delay
    """
    popup_configs = {
        'newsletter': {
            'title': 'Subscribe to Our Newsletter',
            'content': 'Get the latest market updates and investment insights delivered to your inbox.',
            'button': 'Subscribe',
        },
        'alert': {
            'title': 'Important Notice',
            'content': 'Please review our updated terms and conditions.',
            'button': 'I Understand',
        },
        'survey': {
            'title': 'Quick Feedback',
            'content': 'Help us improve by sharing your feedback on this page.',
            'button': 'Take Survey',
        },
    }

    config = popup_configs.get(popup_type, popup_configs['newsletter'])

    popup_data = {
        'type': popup_type,
        'title': config['title'],
        'content': config['content'],
        'button': config['button'],
        'auto_dismiss': auto_dismiss,
        'dismiss_delay': dismiss_delay,
    }

    # Store in session
    session['popup_state'] = popup_data

    return popup_data


def should_show_popup(trigger_condition):
    """
    Check if popup should show based on trigger condition.

    Conditions: 'first_visit', 'data_page', or 'random' (30% chance).

    Args:
        trigger_condition (str): Condition to check ('first_visit', 'data_page', 'random')

    Returns:
        bool: True if popup should be shown, False otherwise
    """
    if trigger_condition == 'first_visit':
        # Check if this is the first visit (no 'visited' flag)
        return not session.get('visited', False)

    elif trigger_condition == 'data_page':
        # Show on data pages if not dismissed
        return not session.get('popup_dismissed', False)

    elif trigger_condition == 'random':
        # Show randomly 30% of the time
        return random.random() < 0.3

    return False


def mark_popup_dismissed():
    """
    Mark popup as dismissed in session and set visited flag.

    Returns:
        None
    """
    session['popup_dismissed'] = True
    session['visited'] = True
