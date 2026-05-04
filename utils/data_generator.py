"""Dynamic data generation utilities."""

import copy
import json
import random


def load_json_data(filepath):
    """
    Load JSON file and return dictionary.

    Args:
        filepath (str): Path to JSON file

    Returns:
        dict: Parsed JSON data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def apply_variance(value, variance_percent=5):
    """
    Apply ±variance_percent random variance to a numeric value.

    Args:
        value (int or float): Original value
        variance_percent (float): Variance percentage (default 5)

    Returns:
        int or float: Value with variance applied, same type as input
    """
    if not isinstance(value, (int, float)):
        return value

    # Calculate variance amount
    variance_amount = value * (variance_percent / 100)

    # Apply random variance within bounds
    variance = random.uniform(-variance_amount, variance_amount)
    new_value = value + variance

    # Return same type as input
    if isinstance(value, int):
        return int(new_value)
    return new_value


def generate_dynamic_aum(aum_data):
    """
    Return copy of AUM data with variance applied to all numeric values.

    Args:
        aum_data (dict): AUM data dictionary

    Returns:
        dict: Copy of AUM data with variance applied
    """
    data_copy = copy.deepcopy(aum_data)

    def apply_variance_recursive(obj):
        """Recursively apply variance to all numeric values."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (int, float)):
                    obj[key] = apply_variance(value)
                elif isinstance(value, (dict, list)):
                    obj[key] = apply_variance_recursive(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, (int, float)):
                    obj[i] = apply_variance(item)
                elif isinstance(item, (dict, list)):
                    obj[i] = apply_variance_recursive(item)
        return obj

    return apply_variance_recursive(data_copy)


def generate_team(team_data, randomize_order=False):
    """
    Return copy of team data, optionally shuffled.

    Args:
        team_data (list): List of team member dictionaries
        randomize_order (bool): Whether to shuffle the team list

    Returns:
        list: Copy of team data, optionally shuffled
    """
    data_copy = copy.deepcopy(team_data)

    if randomize_order:
        random.shuffle(data_copy)

    return data_copy


def get_paginated_data(data_list, page=1, per_page=5):
    """
    Return paginated subset of data.

    Args:
        data_list (list): Full list of items
        page (int): Page number (1-indexed, default 1)
        per_page (int): Items per page (default 5)

    Returns:
        dict: Dictionary with keys:
            - items: List of items for this page
            - page: Current page number
            - per_page: Items per page
            - total: Total number of items
            - total_pages: Total number of pages
    """
    total = len(data_list)
    total_pages = (total + per_page - 1) // per_page  # Ceiling division

    # Clamp page to valid range
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1

    # Calculate slice indices
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    items = data_list[start_idx:end_idx]

    return {
        'items': items,
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
    }
