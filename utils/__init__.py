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
]
