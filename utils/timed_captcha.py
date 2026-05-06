"""Timed CAPTCHA utilities with 30-second expiry."""

import time

from flask import session

from utils.captcha import generate_captcha, validate_captcha


def generate_timed_captcha(sess):
    """
    Generate a CAPTCHA with a timestamp for time-based validation.

    Calls generate_captcha() and stores the issued time in session.

    Args:
        sess: Flask session object

    Returns:
        bytes: CAPTCHA image in PNG format
    """
    captcha_image = generate_captcha()
    sess['captcha_issued_at'] = time.time()
    return captcha_image


def validate_timed_captcha(answer, sess, time_limit=30):
    """
    Validate a CAPTCHA answer with time-based expiry.

    Checks if the CAPTCHA has expired (elapsed time > time_limit).
    If not expired, validates the answer against the stored CAPTCHA.

    Args:
        answer (str): User's CAPTCHA input
        sess: Flask session object
        time_limit (int): Time limit in seconds (default: 30)

    Returns:
        str: 'ok' if validation successful, 'invalid' if answer incorrect, 'expired' if time limit exceeded
    """
    issued_at = sess.get('captcha_issued_at')

    # Check if CAPTCHA was issued
    if issued_at is None:
        return 'invalid'

    # Calculate elapsed time
    elapsed = time.time() - issued_at

    # Check if expired
    if elapsed > time_limit:
        # Clear expired timestamp
        if 'captcha_issued_at' in sess:
            del sess['captcha_issued_at']
        return 'expired'

    # Validate the answer
    is_valid = validate_captcha(answer)

    # Clear timestamp on validation attempt
    if 'captcha_issued_at' in sess:
        del sess['captcha_issued_at']

    return 'ok' if is_valid else 'invalid'
