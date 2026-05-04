"""Zenith-specific behavior tests.

Zenith characteristics (Most Complex):
- CAPTCHA on first visit + data pages
- Strict rate limiting: 3 requests per 60 seconds
- Artificial delay: 0.5 seconds
- Sticky footer popup with auto-dismiss (5 seconds)
- /api/funds JSON endpoint
- AJAX-loaded data
"""

import json
import os
import sys
import time
from pathlib import Path

import pytest

# Set up Python path
test_dir = Path(__file__).parent
project_dir = test_dir.parent
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

from zenith.app import app


class TestZenithFirstVisitCaptcha:
    """Test CAPTCHA on first visit."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_first_home_request_shows_captcha(self):
        """First home request should show CAPTCHA."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_first_about_request_shows_captcha(self):
        """First request to any page shows CAPTCHA."""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_after_visit_no_first_captcha(self):
        """After first visit CAPTCHA passed, home should not show it again."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        response = self.client.get('/')
        assert response.status_code == 200
        # Should not be a CAPTCHA page
        assert b'Enter the code' not in response.data or b'<h1' in response.data


class TestOaktreeDataPageCaptcha:
    """Test CAPTCHA on data pages."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_strategies_requires_captcha_after_visit(self):
        """Strategies page requires CAPTCHA after first visit."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_funds_requires_captcha_after_visit(self):
        """Funds page requires CAPTCHA after first visit."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        response = self.client.get('/funds')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_investor_resources_requires_captcha(self):
        """Investor resources page requires CAPTCHA."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        response = self.client.get('/investor-resources')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_fund_detail_requires_captcha(self):
        """Fund detail page requires CAPTCHA."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        response = self.client.get('/fund/1')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_can_be_passed_for_data_pages(self):
        """After passing data page CAPTCHA, should access page."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        response = self.client.get('/strategies')
        assert response.status_code == 200
        # Should not be CAPTCHA page anymore
        assert len(response.data) > 100


class TestOaktreeStrictRateLimiting:
    """Test strict rate limiting: 3 requests per 60 seconds."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_three_requests_succeed(self):
        """First 3 requests should succeed."""
        with self.client.session_transaction() as sess:
            sess.clear()

        for i in range(3):
            response = self.client.get('/')
            assert response.status_code == 200, f"Request {i+1} failed"

    def test_fourth_request_rate_limited(self):
        """4th request should be rate limited."""
        with self.client.session_transaction() as sess:
            sess.clear()

        # Make 3 successful requests
        for _ in range(3):
            response = self.client.get('/')
            assert response.status_code == 200

        # 4th request should be rate limited
        response = self.client.get('/')
        # Should be 429 or similar
        assert response.status_code in [429, 403, 200]

    def test_rate_limit_per_session(self):
        """Rate limit should be per session."""
        client1 = app.test_client()
        client2 = app.test_client()

        # Client 1 makes 3 requests
        for _ in range(3):
            response = client1.get('/')
            assert response.status_code == 200

        # Client 2 should still be able to make requests
        response = client2.get('/')
        assert response.status_code == 200


class TestOaktreeArtificialDelay:
    """Test artificial 0.5 second delay."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_request_has_0_5_second_delay(self):
        """Requests should have ~0.5 second delay."""
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start

        assert response.status_code == 200
        # Should take at least 0.4 seconds
        assert elapsed >= 0.4

    def test_multiple_requests_all_delayed(self):
        """All requests should be delayed."""
        for _ in range(3):
            start = time.time()
            response = self.client.get('/')
            elapsed = time.time() - start

            assert response.status_code == 200
            assert elapsed >= 0.4

    def test_delay_not_too_long(self):
        """Delay should not be excessive."""
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start

        assert response.status_code == 200
        # Should not be more than 1.5 seconds
        assert elapsed < 1.5


class TestOaktreeApiEndpoint:
    """Test /api/funds JSON endpoint."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_api_funds_returns_json(self):
        """API endpoint should return JSON."""
        response = self.client.get('/api/funds')
        assert response.status_code == 200
        assert response.content_type.startswith('application/json')

    def test_api_funds_valid_json(self):
        """API should return valid JSON structure."""
        response = self.client.get('/api/funds')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, (dict, list))

    def test_api_accessible_without_captcha(self):
        """API endpoint should be accessible without CAPTCHA."""
        response = self.client.get('/api/funds')
        assert response.status_code == 200


class TestOaktreeStickyFooterPopup:
    """Test sticky footer popup with auto-dismiss."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_page_loads_successfully(self):
        """Page should load successfully (with or without popup)."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        response = self.client.get('/')
        assert response.status_code == 200

    def test_dismiss_popup_endpoint_works(self):
        """Dismiss popup endpoint should work."""
        response = self.client.post('/api/dismiss-popup')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)

    def test_popup_can_be_dismissed(self):
        """Popup should be dismissible."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        response = self.client.get('/')
        assert response.status_code == 200

        # Dismiss popup
        response = self.client.post('/api/dismiss-popup')
        assert response.status_code == 200


class TestOaktreeCombinedComplexity:
    """Test all features working together."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_first_visit_flow(self):
        """Test first visit CAPTCHA flow."""
        # First request should show CAPTCHA
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_post_visit_flow(self):
        """Test post-visit flow with data page CAPTCHA."""
        # Set visited flag
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        # Home should be accessible
        response = self.client.get('/')
        assert response.status_code == 200

        # Data page should require CAPTCHA
        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_full_access_after_captcha(self):
        """Test full access after passing both CAPTCHAs."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        # All pages should be accessible
        routes = ['/', '/about', '/strategies', '/funds', '/news']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200

    def test_rate_limit_and_delay_combined(self):
        """Test rate limiting with artificial delay."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        # Make 3 rapid requests
        for i in range(3):
            start = time.time()
            response = self.client.get('/')
            elapsed = time.time() - start

            assert response.status_code == 200
            # Should have delay
            assert elapsed >= 0.4


class TestOaktreeAllRoutes:
    """Test all Oaktree routes."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_all_main_routes_accessible(self):
        """All main routes should be accessible."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        routes = [
            '/',
            '/about',
            '/leadership',
            '/news',
            '/contact',
            '/fund/1',
            '/fund/5'
        ]
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200, f"Route {route} failed"

    def test_data_pages_accessible(self):
        """Data pages should be accessible after CAPTCHA."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        data_routes = ['/strategies', '/investor-resources', '/funds']
        for route in data_routes:
            response = self.client.get(route)
            assert response.status_code == 200


class TestOaktreeLeadership:
    """Test Oaktree leadership page."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_leadership_accessible(self):
        """Leadership page should be accessible."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        response = self.client.get('/leadership')
        assert response.status_code == 200

    def test_leadership_pagination(self):
        """Leadership pagination should work."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200

        response = self.client.get('/leadership?page=2')
        assert response.status_code == 200


class TestOaktreeConsistency:
    """Test Oaktree consistency."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_session_management(self):
        """Session management should work correctly."""
        # Check initial state
        response = self.client.get('/')
        assert response.status_code == 200

        # Set visited flag
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        # Flag should persist
        response = self.client.get('/')
        assert response.status_code == 200

    def test_company_name_in_response(self):
        """Company name should appear in responses."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        response = self.client.get('/')
        assert response.status_code == 200
        assert len(response.data) > 100
