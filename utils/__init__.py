"""Shared utilities package for mock financial websites."""

from utils.captcha import generate_captcha, validate_captcha
from utils.data_generator import (
    apply_variance,
    generate_dynamic_aum,
    generate_team,
    get_paginated_data,
    load_json_data,
)
from utils.popups import mark_popup_dismissed, render_popup, should_show_popup
from utils.rate_limit import rate_limit
from utils.javascript_validation import require_javascript, inject_js_routes, generate_js_token
from utils.cookie_validation import inject_cookie_middleware, get_required_cookie_value
from utils.user_agent_check import block_user_agent, inject_user_agent_middleware, is_blocked_user_agent
from utils.strict_headers import require_headers, inject_headers_middleware, has_required_headers
from utils.auth_utils import generate_jwt_token, verify_jwt_token, require_login, authenticate_user
from utils.honeypot import generate_honeypot_field_name, inject_honeypot_fields, validate_form_submission
from utils.geoip_utils import get_country_from_ip, is_vpn_ip, allow_countries, block_vpn, inject_geoip_routes
from utils.dynamic_urls import get_random_slug, get_random_slug_suffix, is_valid_slug, inject_url_helpers
from utils.cookie_banner import (
    require_cookie_acceptance,
    inject_cookie_banner_routes,
    is_cookie_accepted,
    is_banner_dismissed,
    BANNER_MODES,
)

__all__ = [
    'generate_captcha',
    'validate_captcha',
    'render_popup',
    'should_show_popup',
    'mark_popup_dismissed',
    'generate_dynamic_aum',
    'generate_team',
    'load_json_data',
    'apply_variance',
    'get_paginated_data',
    'rate_limit',
    'require_javascript',
    'inject_js_routes',
    'generate_js_token',
    'inject_cookie_middleware',
    'get_required_cookie_value',
    'block_user_agent',
    'inject_user_agent_middleware',
    'is_blocked_user_agent',
    'require_headers',
    'inject_headers_middleware',
    'has_required_headers',
    'generate_jwt_token',
    'verify_jwt_token',
    'require_login',
    'authenticate_user',
    'generate_honeypot_field_name',
    'inject_honeypot_fields',
    'validate_form_submission',
    'get_country_from_ip',
    'is_vpn_ip',
    'allow_countries',
    'block_vpn',
    'inject_geoip_routes',
    'get_random_slug',
    'get_random_slug_suffix',
    'is_valid_slug',
    'inject_url_helpers',
    'require_cookie_acceptance',
    'inject_cookie_banner_routes',
    'is_cookie_accepted',
    'is_banner_dismissed',
    'BANNER_MODES',
]
