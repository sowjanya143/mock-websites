"""Test suite for shared utilities."""

import pytest

from utils.data_generator import apply_variance, get_paginated_data


class TestApplyVariance:
    """Tests for apply_variance function."""

    def test_apply_variance_int(self):
        """Test variance applied to integer 1000 produces value in range 950-1050."""
        value = 1000
        variance_percent = 5

        # Test multiple times to account for randomness
        for _ in range(100):
            result = apply_variance(value, variance_percent)

            # Check that result is within expected range (±5%)
            assert 950 <= result <= 1050, f"Result {result} outside range 950-1050"

            # Check that result is an integer
            assert isinstance(result, int), f"Result {result} is not an integer"

    def test_apply_variance_float(self):
        """Test variance applied to float produces float."""
        value = 1000.0
        variance_percent = 5

        result = apply_variance(value, variance_percent)

        # Check that result is within expected range
        assert 950 <= result <= 1050, f"Result {result} outside range 950-1050"

        # Check that result is a float
        assert isinstance(result, float), f"Result {result} is not a float"

    def test_apply_variance_zero_variance(self):
        """Test that zero variance returns original value."""
        value = 1000
        result = apply_variance(value, variance_percent=0)
        assert result == value

    def test_apply_variance_non_numeric(self):
        """Test that non-numeric values are returned unchanged."""
        value = "not a number"
        result = apply_variance(value)
        assert result == value


class TestGetPaginatedData:
    """Tests for get_paginated_data function."""

    def test_get_paginated_data_basic(self):
        """Test pagination works correctly (25 items, 5 per page = 5 total pages)."""
        data = list(range(1, 26))  # 25 items: [1, 2, ..., 25]

        result = get_paginated_data(data, page=1, per_page=5)

        assert result['page'] == 1
        assert result['per_page'] == 5
        assert result['total'] == 25
        assert result['total_pages'] == 5
        assert result['items'] == [1, 2, 3, 4, 5]

    def test_get_paginated_data_page_3(self):
        """Test that page 3 returns items 11-15."""
        data = list(range(1, 26))  # 25 items: [1, 2, ..., 25]

        result = get_paginated_data(data, page=3, per_page=5)

        assert result['page'] == 3
        assert result['total_pages'] == 5
        assert result['items'] == [11, 12, 13, 14, 15]

    def test_get_paginated_data_last_page(self):
        """Test last page with partial items."""
        data = list(range(1, 26))  # 25 items: [1, 2, ..., 25]

        result = get_paginated_data(data, page=5, per_page=5)

        assert result['page'] == 5
        assert result['total_pages'] == 5
        assert result['items'] == [21, 22, 23, 24, 25]

    def test_get_paginated_data_out_of_range(self):
        """Test that out-of-range page is clamped to valid range."""
        data = list(range(1, 26))  # 25 items

        result = get_paginated_data(data, page=10, per_page=5)

        # Should be clamped to last page
        assert result['page'] == 5
        assert result['items'] == [21, 22, 23, 24, 25]

    def test_get_paginated_data_empty_list(self):
        """Test pagination with empty list."""
        data = []

        result = get_paginated_data(data, page=1, per_page=5)

        assert result['page'] == 1
        assert result['per_page'] == 5
        assert result['total'] == 0
        assert result['total_pages'] == 0
        assert result['items'] == []

    def test_get_paginated_data_single_page(self):
        """Test data smaller than page size fits on one page."""
        data = [1, 2, 3]

        result = get_paginated_data(data, page=1, per_page=5)

        assert result['total_pages'] == 1
        assert result['items'] == [1, 2, 3]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
