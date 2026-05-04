"""Rate limiting utilities."""

import time
from functools import wraps

from flask import request
from werkzeug.exceptions import TooManyRequests

# Global store for request times by IP
_request_times = {}


def rate_limit(max_requests=10, time_window=60):
    """
    Decorator that tracks per-IP requests and returns 429 if limit exceeded.

    Args:
        max_requests (int): Maximum requests allowed in time window (default 10)
        time_window (int): Time window in seconds (default 60)

    Returns:
        function: Decorator function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr

            current_time = time.time()

            # Initialize or get request times for this IP
            if client_ip not in _request_times:
                _request_times[client_ip] = []

            # Clean old entries outside time window
            _request_times[client_ip] = [
                t for t in _request_times[client_ip] if current_time - t < time_window
            ]

            # Check if limit exceeded
            if len(_request_times[client_ip]) >= max_requests:
                raise TooManyRequests(
                    f'Rate limit exceeded: {max_requests} requests per {time_window} seconds'
                )

            # Record this request
            _request_times[client_ip].append(current_time)

            # Call the original function
            return func(*args, **kwargs)

        return wrapper

    return decorator
