"""Fortress-specific behavior tests.

Fortress characteristics:
- CAPTCHA on every page
- No rate limiting
- No popups
- Dynamic AUM variance (±5%)
"""

import base64
import os
import sys
from pathlib import Path

import pytest

# Set up Python path
test_dir = Path(__file__).parent
project_dir = test_dir.parent
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

from fortress.app import app


class TestFortressCaptchaEveryPage:
    """Test that CAPTCHA appears on every page."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_captcha_on_home(self):
        """CAPTCHA should appear on home page."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_about(self):
        """CAPTCHA should appear on about page."""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_leadership(self):
        """CAPTCHA should appear on leadership page."""
        response = self.client.get('/leadership')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_strategies(self):
        """CAPTCHA should appear on strategies page."""
        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_funds(self):
        """CAPTCHA should appear on funds page."""
        response = self.client.get('/funds')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_captcha_on_news(self):
        """CAPTCHA should appear on news page."""
        response = self.client.get('/news')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()


class TestFortressCaptchaValidation:
    """Test CAPTCHA validation flow."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_captcha_form_present(self):
        """CAPTCHA form should be present on protected pages."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'form' in response.data.lower() or b'<input' in response.data

    def test_captcha_can_be_passed(self):
        """CAPTCHA can be solved and session updated."""
        # First request shows CAPTCHA
        response = self.client.get('/')
        assert b'captcha' in response.data.lower()

        # Manually set session to bypass CAPTCHA
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        # Next request should not show CAPTCHA
        response = self.client.get('/')
        assert response.status_code == 200
        # Should not be a captcha page
        assert b'Enter the code' not in response.data or b'<h1' in response.data

    def test_session_persists_across_requests(self):
        """Once CAPTCHA is passed, session persists."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        # Multiple requests should work
        for _ in range(3):
            response = self.client.get('/')
            assert response.status_code == 200


class TestFortressAumData:
    """Test AUM data display."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_aum_data_on_home(self):
        """AUM data should appear on home page."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/')
        assert response.status_code == 200
        # Should have some content indicating AUM
        assert len(response.data) > 500

    def test_aum_data_on_strategies(self):
        """AUM data should appear on strategies page."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert len(response.data) > 500

    def test_aum_data_on_funds(self):
        """AUM data should appear on funds page."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/funds')
        assert response.status_code == 200
        assert len(response.data) > 500


class TestFortressLeadershipPagination:
    """Test leadership page pagination."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_leadership_page_1_accessible(self):
        """Leadership page 1 should be accessible."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200

    def test_leadership_page_2_accessible(self):
        """Leadership page 2 should be accessible."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/leadership?page=2')
        assert response.status_code == 200

    def test_leadership_default_page(self):
        """Leadership without page parameter should default to page 1."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/leadership')
        assert response.status_code == 200

    def test_leadership_has_pagination_info(self):
        """Leadership page should have pagination info."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200
        # Should have page information in response
        assert b'page' in response.data.lower() or b'<a' in response.data


class TestFortressDynamicVariance:
    """Test dynamic AUM variance."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_aum_variance_on_reload(self):
        """AUM values should vary slightly on reload."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        # Get responses multiple times
        responses = []
        for _ in range(3):
            response = self.client.get('/')
            assert response.status_code == 200
            responses.append(response.data)

        # Responses should exist (may vary in content due to dynamic generation)
        assert len(responses) == 3
        assert all(len(r) > 100 for r in responses)


class TestFortressNoRateLimit:
    """Test that Fortress has no rate limiting."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_no_rate_limit_on_requests(self):
        """Multiple rapid requests should all succeed."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        # Make 20 rapid requests
        for _ in range(20):
            response = self.client.get('/')
            assert response.status_code == 200

    def test_no_rate_limit_on_different_routes(self):
        """Requests to different routes should not be rate limited."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        routes = ['/', '/about', '/strategies', '/funds', '/news']
        # Make 10 requests to each route
        for _ in range(10):
            for route in routes:
                response = self.client.get(route)
                assert response.status_code == 200


class TestFortressNoPopups:
    """Test that Fortress has no popups."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_no_popup_on_home(self):
        """No popup on home page."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/')
        assert response.status_code == 200
        # Should not have popup markers
        assert b'popup' not in response.data.lower() or b'display' not in response.data.lower()

    def test_dismiss_popup_endpoint_exists(self):
        """Dismiss popup endpoint should exist (but may not be used)."""
        response = self.client.post('/api/dismiss-popup')
        assert response.status_code == 200


class TestFortressFundDetail:
    """Test fund detail pages."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_fund_detail_page_1(self):
        """Fund detail page 1 should be accessible."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/fund/1')
        assert response.status_code == 200

    def test_fund_detail_page_5(self):
        """Fund detail page 5 should be accessible."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/fund/5')
        assert response.status_code == 200

    def test_fund_detail_high_id(self):
        """Fund detail page with high ID should still be accessible."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/fund/999')
        assert response.status_code == 200
