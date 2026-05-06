"""DOM obfuscation - randomizes CSS class names per session."""

import random
import string
from flask import session

def generate_class_map(sess):
    """Generate mapping of semantic class names to random 5-char strings.

    Returns existing map if already in session.

    Args:
        sess: Flask session object

    Returns:
        dict: {semantic_name: random_5char}
    """
    if 'class_map' in sess:
        return sess['class_map']

    class_map = {
        'aum-value': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'fund-name': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'strategy-title': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'data-table': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
        'aum-stat': ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
    }

    sess['class_map'] = class_map
    return class_map


def inject_dom_obfuscator(app):
    """Inject class_map into all templates via context processor."""

    @app.context_processor
    def inject_class_map():
        class_map = generate_class_map(session)
        return {'class_map': class_map}
