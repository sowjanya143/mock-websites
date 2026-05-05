"""Dynamic URL generation - rotating route slugs."""

import random
import string


# URL slug mappings - maps canonical routes to rotating slugs
URL_SLUG_MAP = {
    'home': ['', 'dashboard', 'index', 'main'],
    'about': ['about', 'company', 'team-info', 'info'],
    'leadership': ['leadership', 'team', 'management', 'executives'],
    'strategies': ['strategies', 'approach', 'methods', 'portfolio'],
    'investor_resources': ['investor-resources', 'resources', 'documents', 'materials'],
    'funds': ['funds', 'investments', 'products', 'offerings'],
    'news': ['news', 'blog', 'updates', 'press'],
    'contact': ['contact', 'support', 'reach-us', 'connect'],
}


def get_random_slug(canonical_name):
    """Get a random slug for a canonical route name."""
    if canonical_name not in URL_SLUG_MAP:
        return canonical_name

    slugs = URL_SLUG_MAP[canonical_name]
    return random.choice(slugs)


def get_random_slug_suffix(length=6):
    """Generate a random suffix for obfuscation."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def is_valid_slug(slug, canonical_name):
    """Check if a slug maps to a canonical name."""
    if canonical_name not in URL_SLUG_MAP:
        return False

    return slug in URL_SLUG_MAP[canonical_name]


def inject_url_helpers(app):
    """Inject URL helpers into Flask app context."""

    @app.context_processor
    def inject_url_functions():
        """Make URL functions available in templates."""
        return {
            'get_random_slug': get_random_slug,
        }
