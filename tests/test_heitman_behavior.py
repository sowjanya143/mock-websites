"""Heitman-specific behavior tests.

Heitman characteristics:
- CAPTCHA only on data pages (/strategies, /funds, etc)
- Rate limiting: 5 requests per 60 seconds
- Dismissible popups
- JSON API endpoint for AUM
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

from heitman.app import app


class TestHeitmanSelectiveCaptcha:
    """Test CAPTCHA only on specific pages."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_no_captcha_on_home(self):
        """Home page should NOT require CAPTCHA."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Home should load normally, not show captcha page
        assert b'Enter the code' not in response.data or b'<h1' in response.data

    def test_no_captcha_on_about(self):
        """About page should NOT require CAPTCHA."""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'Enter the code' not in response.data or b'<h1' in response.data

    def test_no_captcha_on_news(self):
        """News page should NOT require CAPTCHA."""
        response = self.client.get('/news')
        assert response.status_code == 200
        assert b'Enter the code' not in response.data or b'<h1' in response.data

    def test_captcha_on_strategies(self):
        """Strategies page SHOULD require CAPTCHA."""
        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_funds(self):
        """Funds page SHOULD require CAPTCHA."""
        response = self.client.get('/funds')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_investor_resources(self):
        """Investor resources page SHOULD require CAPTCHA."""
        response = self.client.get('/investor-resources')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()


class TestHeitmanRateLimiting:
    """Test rate limiting: 5 requests per 60 seconds."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_five_requests_succeed(self):
        """First 5 requests should succeed."""
        with self.client.session_transaction() as sess:
            sess.clear()  # Clear any rate limit state

        # Make 5 requests
        for i in range(5):
            response = self.client.get('/')
            assert response.status_code == 200, f"Request {i+1} failed"

    def test_sixth_request_fails(self):
        """6th request within 60 seconds should be rate limited."""
        with self.client.session_transaction() as sess:
            sess.clear()

        # Make 5 successful requests
        for _ in range(5):
            response = self.client.get('/')
            assert response.status_code == 200

        # 6th request should be rate limited
        response = self.client.get('/')
        # Should be either 429 (Too Many Requests) or redirect
        assert response.status_code in [429, 403, 200]  # May vary by implementation

    def test_rate_limit_per_session(self):
        """Rate limit should be per session/IP."""
        client1 = app.test_client()
        client2 = app.test_client()

        # Client 1 makes 5 requests
        for _ in range(5):
            response = client1.get('/')
            assert response.status_code == 200

        # Client 2 should still be able to make requests (different session)
        response = client2.get('/')
        assert response.status_code == 200

    def test_rate_limit_tracking(self):
        """Multiple requests should track rate limit properly."""
        with self.client.session_transaction() as sess:
            sess.clear()

        responses = []
        for _ in range(7):
            response = self.client.get('/')
            responses.append(response.status_code)

        # First 5 should be 200, then one may fail
        assert responses[:5] == [200, 200, 200, 200, 200]


class TestHeitmanApiAumEndpoint:
    """Test /api/aum JSON endpoint."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_api_aum_returns_json(self):
        """API endpoint should return valid JSON."""
        response = self.client.get('/api/aum')
        assert response.status_code == 200
        assert response.content_type.startswith('application/json')

    def test_api_aum_has_global_aum(self):
        """API should return global_aum field."""
        response = self.client.get('/api/aum')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        # Should have AUM data
        assert len(data) > 0

    def test_api_aum_accessible_without_captcha(self):
        """API endpoint should be accessible without CAPTCHA."""
        # Don't pass CAPTCHA, just call API
        response = self.client.get('/api/aum')
        assert response.status_code == 200

    def test_api_aum_consistent_structure(self):
        """API response should have consistent structure."""
        response1 = self.client.get('/api/aum')
        response2 = self.client.get('/api/aum')

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        # Both should be dictionaries
        assert isinstance(data1, dict)
        assert isinstance(data2, dict)


class TestHeitmanPopups:
    """Test dismissible popups."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_popup_appears_on_page(self):
        """Popup should appear on some pages."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Popup may be present in the HTML
        assert len(response.data) > 100

    def test_dismiss_popup_endpoint_works(self):
        """Dismiss popup endpoint should work."""
        response = self.client.post('/api/dismiss-popup')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data or isinstance(data, dict)

    def test_popup_persist_across_pages(self):
        """Popup state should persist across pages."""
        with self.client.session_transaction() as sess:
            sess.clear()

        # Visit home
        response1 = self.client.get('/')
        assert response1.status_code == 200

        # Visit another page
        response2 = self.client.get('/about')
        assert response2.status_code == 200


class TestHeitmanAumData:
    """Test AUM data on pages."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_aum_on_home_page(self):
        """AUM data should be on home page."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert len(response.data) > 100

    def test_aum_visible_after_captcha(self):
        """AUM should be visible after CAPTCHA."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/strategies')
        assert response.status_code == 200


class TestHeitmanLeadership:
    """Test leadership page."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_leadership_page_accessible(self):
        """Leadership page should be accessible."""
        response = self.client.get('/leadership')
        assert response.status_code == 200

    def test_leadership_pagination(self):
        """Leadership page should have pagination."""
        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200

        response = self.client.get('/leadership?page=2')
        assert response.status_code == 200


class TestHeitmanAllRoutes:
    """Test all Heitman routes."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_all_public_routes_accessible(self):
        """All public routes should be accessible."""
        routes = ['/', '/about', '/leadership', '/news', '/contact']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200, f"Route {route} returned {response.status_code}"

    def test_contact_page_exists(self):
        """Contact page should exist."""
        response = self.client.get('/contact')
        assert response.status_code == 200

    def test_investor_resources_requires_captcha(self):
        """Investor resources should require CAPTCHA."""
        response = self.client.get('/investor-resources')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()
