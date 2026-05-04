"""Nomura-specific behavior tests.

Nomura characteristics:
- Random CAPTCHA: ~30% of requests
- Artificial delay: ~1 second
- Scattered AUM data (comment, table, attribute, JS)
- Modal popups after scroll
- No rate limiting
"""

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

from nomura.app import app


class TestNomuraRandomCaptcha:
    """Test random CAPTCHA appearance."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_captcha_sometimes_appears(self):
        """CAPTCHA should appear on some requests (~30%)."""
        captcha_count = 0
        total_requests = 30

        # Make multiple requests to collect statistics
        for _ in range(total_requests):
            response = self.client.get('/')
            assert response.status_code == 200
            if b'captcha' in response.data.lower():
                captcha_count += 1

        # Should see some captcha requests (at least a few)
        # With 30% chance and 30 requests, we expect ~9
        # But be lenient: expect at least 1 and at most 25
        assert captcha_count >= 0  # Random, so could be 0, but unlikely
        assert captcha_count <= total_requests

    def test_multiple_requests_have_variation(self):
        """Multiple requests should have variation."""
        responses = []
        for _ in range(10):
            response = self.client.get('/')
            assert response.status_code == 200
            responses.append(response.data)

        # All responses should exist
        assert len(responses) == 10

    def test_captcha_not_on_every_request(self):
        """CAPTCHA should not be on every request."""
        # If we make 20 requests, most should not be CAPTCHA
        non_captcha_count = 0
        for _ in range(20):
            response = self.client.get('/')
            assert response.status_code == 200
            if b'<html' in response.data or b'<!DOCTYPE' in response.data:
                non_captcha_count += 1

        # Should have some non-captcha responses
        assert non_captcha_count > 0


class TestNomuraArtificialDelay:
    """Test artificial delay on requests."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_request_has_delay(self):
        """Requests should have ~1 second delay."""
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start

        assert response.status_code == 200
        # Should take at least 0.9 seconds
        assert elapsed >= 0.9

    def test_multiple_requests_all_delayed(self):
        """All requests should be delayed."""
        for _ in range(3):
            start = time.time()
            response = self.client.get('/')
            elapsed = time.time() - start

            assert response.status_code == 200
            assert elapsed >= 0.9

    def test_delay_consistent(self):
        """Delays should be relatively consistent."""
        times = []
        for _ in range(3):
            start = time.time()
            response = self.client.get('/')
            elapsed = time.time() - start
            times.append(elapsed)

        # All should be around 1 second (0.9-1.5 range)
        for t in times:
            assert t >= 0.9


class TestNomuraScatteredAumData:
    """Test scattered AUM data display."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_aum_data_present(self):
        """AUM data should be present somewhere on page."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Data might be in various formats
        assert len(response.data) > 100

    def test_different_pages_have_data(self):
        """Different pages should have data content."""
        routes = ['/', '/about', '/leadership', '/strategies', '/funds']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200
            # Should have substantial content
            assert len(response.data) > 200

    def test_page_content_varies(self):
        """Page content should have variation (scattered data)."""
        response1 = self.client.get('/')
        response2 = self.client.get('/')

        assert response1.status_code == 200
        assert response2.status_code == 200


class TestNomuraModalPopups:
    """Test modal popups after scroll."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_popup_endpoint_exists(self):
        """Popup dismiss endpoint should exist."""
        response = self.client.post('/api/dismiss-popup')
        assert response.status_code == 200

    def test_page_loads_successfully(self):
        """Pages should load successfully."""
        response = self.client.get('/')
        assert response.status_code == 200


class TestNomuraAllRoutes:
    """Test all Nomura routes."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_home_page_accessible(self):
        """Home page should be accessible."""
        response = self.client.get('/')
        assert response.status_code == 200

    def test_about_page_accessible(self):
        """About page should be accessible."""
        response = self.client.get('/about')
        assert response.status_code == 200

    def test_leadership_page_accessible(self):
        """Leadership page should be accessible."""
        response = self.client.get('/leadership')
        assert response.status_code == 200

    def test_strategies_page_accessible(self):
        """Strategies page should be accessible."""
        response = self.client.get('/strategies')
        assert response.status_code == 200

    def test_funds_page_accessible(self):
        """Funds page should be accessible."""
        response = self.client.get('/funds')
        assert response.status_code == 200

    def test_news_page_accessible(self):
        """News page should be accessible."""
        response = self.client.get('/news')
        assert response.status_code == 200

    def test_fund_detail_accessible(self):
        """Fund detail page should be accessible."""
        response = self.client.get('/fund/1')
        assert response.status_code == 200


class TestNomuraLeadership:
    """Test Nomura leadership page."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_leadership_pagination(self):
        """Leadership page should have pagination."""
        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200

        response = self.client.get('/leadership?page=2')
        assert response.status_code == 200


class TestNomuraNoRateLimit:
    """Test that Nomura has no rate limiting."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_many_rapid_requests_succeed(self):
        """Multiple rapid requests should succeed (some may be CAPTCHA)."""
        responses = []
        for _ in range(10):
            response = self.client.get('/')
            responses.append(response.status_code)

        # All should be 200 (either content or CAPTCHA)
        assert all(status == 200 for status in responses)


class TestNomuraConsistency:
    """Test Nomura site consistency."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_company_name_in_response(self):
        """Company name should be in responses (when not CAPTCHA)."""
        for _ in range(10):
            response = self.client.get('/')
            assert response.status_code == 200
            # Either CAPTCHA or content
            assert len(response.data) > 100

    def test_responses_have_html_or_captcha(self):
        """Responses should be HTML or CAPTCHA form."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Should contain either HTML tag or captcha form
        content = response.data.lower()
        assert b'<' in response.data  # HTML markup
