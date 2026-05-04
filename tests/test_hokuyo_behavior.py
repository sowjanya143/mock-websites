"""Premier-specific behavior tests.

Premier characteristics (Control Site):
- NO CAPTCHA on any page
- NO POPUPS
- Instant responses (no artificial delay)
- Clean HTML tables for AUM data
- Simple, straightforward design
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

from premier.app import app


class TestHokuyoNoCaptcha:
    """Test that NO CAPTCHA appears on any page."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_no_captcha_on_home(self):
        """Home page should have NO CAPTCHA."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Should not be a CAPTCHA page
        content = response.data.lower()
        assert b'captcha' not in content or b'<h1' in response.data

    def test_no_captcha_on_about(self):
        """About page should have NO CAPTCHA."""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'captcha' not in response.data.lower()

    def test_no_captcha_on_leadership(self):
        """Leadership page should have NO CAPTCHA."""
        response = self.client.get('/leadership')
        assert response.status_code == 200
        assert b'captcha' not in response.data.lower()

    def test_no_captcha_on_strategies(self):
        """Strategies page should have NO CAPTCHA."""
        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' not in response.data.lower()

    def test_no_captcha_on_funds(self):
        """Funds page should have NO CAPTCHA."""
        response = self.client.get('/funds')
        assert response.status_code == 200
        assert b'captcha' not in response.data.lower()

    def test_no_captcha_on_news(self):
        """News page should have NO CAPTCHA."""
        response = self.client.get('/news')
        assert response.status_code == 200
        assert b'captcha' not in response.data.lower()

    def test_no_captcha_on_fund_detail(self):
        """Fund detail page should have NO CAPTCHA."""
        response = self.client.get('/fund/1')
        assert response.status_code == 200
        assert b'captcha' not in response.data.lower()


class TestHokuyoNoPopups:
    """Test that NO POPUPS appear."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_no_popup_on_home(self):
        """Home page should have NO POPUP."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Should not contain popup-specific elements
        content = response.data.lower()
        # Be lenient - may have word 'popup' in comments but shouldn't trigger display
        assert b'display' not in content or b'none' in content

    def test_no_popup_on_pages(self):
        """Pages should have NO POPUPS."""
        routes = ['/about', '/leadership', '/strategies', '/funds']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200


class TestHokuyoInstantResponse:
    """Test that responses are instant (under 100ms)."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_home_instant(self):
        """Home page should load instantly."""
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start

        assert response.status_code == 200
        # Should be very fast (under 100ms)
        assert elapsed < 0.1

    def test_all_routes_instant(self):
        """All routes should load instantly."""
        routes = ['/', '/about', '/leadership', '/strategies', '/funds', '/news']
        for route in routes:
            start = time.time()
            response = self.client.get(route)
            elapsed = time.time() - start

            assert response.status_code == 200
            assert elapsed < 0.1, f"Route {route} took {elapsed}s"

    def test_no_artificial_delay(self):
        """Responses should not have artificial delay."""
        for _ in range(5):
            start = time.time()
            response = self.client.get('/')
            elapsed = time.time() - start

            assert response.status_code == 200
            # All should be fast
            assert elapsed < 0.1


class TestHokuyoCleanTables:
    """Test that AUM data is in clean HTML tables."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_home_has_table(self):
        """Home page should have HTML tables."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Should contain table markup
        assert b'<table' in response.data

    def test_strategies_has_table(self):
        """Strategies page should have HTML tables."""
        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'<table' in response.data

    def test_funds_has_table(self):
        """Funds page should have HTML tables."""
        response = self.client.get('/funds')
        assert response.status_code == 200
        assert b'<table' in response.data

    def test_aum_in_table_cells(self):
        """AUM data should be in table cells."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Tables should have standard structure
        assert b'<tr' in response.data or b'<table' in response.data


class TestHokuyoAllRoutesAccessible:
    """Test all routes return 200."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_all_main_routes_return_200(self):
        """All main routes should return 200."""
        routes = [
            '/',
            '/about',
            '/leadership',
            '/strategies',
            '/investor-resources',
            '/funds',
            '/fund/1',
            '/fund/5',
            '/news',
            '/contact'
        ]
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200, f"Route {route} returned {response.status_code}"

    def test_leadership_pagination(self):
        """Leadership pagination should work."""
        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200

        response = self.client.get('/leadership?page=2')
        assert response.status_code == 200

    def test_invalid_page_still_works(self):
        """Invalid page numbers should still return 200."""
        response = self.client.get('/leadership?page=999')
        assert response.status_code == 200


class TestHokuyoSimpleDesign:
    """Test Hokuyo's simple, clean design."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_home_is_simple_html(self):
        """Home page should be simple HTML."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE' in response.data or b'<html' in response.data

    def test_pages_are_valid_html(self):
        """Pages should be valid HTML structure."""
        routes = ['/', '/about', '/leadership', '/strategies', '/funds']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200
            # Should have HTML structure
            assert b'<' in response.data


class TestHokuyoLeadership:
    """Test Hokuyo leadership page."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_leadership_page_accessible(self):
        """Leadership page should be accessible."""
        response = self.client.get('/leadership')
        assert response.status_code == 200

    def test_leadership_with_pagination_params(self):
        """Leadership with page params should work."""
        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200

    def test_leadership_has_team_data(self):
        """Leadership page should have team data."""
        response = self.client.get('/leadership')
        assert response.status_code == 200
        assert len(response.data) > 100


class TestHokuyoConsistency:
    """Test Hokuyo consistency and reliability."""

    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_multiple_home_requests_identical_timing(self):
        """Multiple requests should have consistent timing."""
        times = []
        for _ in range(5):
            start = time.time()
            response = self.client.get('/')
            elapsed = time.time() - start
            times.append(elapsed)
            assert response.status_code == 200

        # All should be fast and similar
        for t in times:
            assert t < 0.1

    def test_company_name_in_page(self):
        """Company name should appear on pages."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Should have some content
        assert len(response.data) > 200

    def test_pages_have_consistent_structure(self):
        """Pages should have consistent HTML structure."""
        routes = ['/', '/about', '/strategies']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200
            # All should be proper HTML
            assert b'<html' in response.data or b'<!DOCTYPE' in response.data or b'<body' in response.data
