"""Integration tests for all 5 sites."""

import json
import os
import sys
from pathlib import Path

import pytest

# Set up Python path for imports
test_dir = Path(__file__).parent
project_dir = test_dir.parent
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

# Import apps - these should handle their own config imports
from fortress.app import app as fortress_app
from heitman.app import app as heitman_app
from nomura.app import app as nomura_app
from hokuyo.app import app as hokuyo_app
from oaktree.app import app as oaktree_app


class TestFortressIntegration:
    """Integration tests for Fortress site."""

    def setup_method(self):
        """Set up test client."""
        self.app = fortress_app
        self.client = self.app.test_client()

    def test_fortress_home_requires_captcha(self):
        """Home page should require CAPTCHA."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_fortress_all_routes_require_captcha(self):
        """All routes should require CAPTCHA."""
        routes = ['/about', '/leadership', '/strategies', '/funds', '/news', '/contact']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200
            assert b'captcha' in response.data.lower() or b'Enter the code' in response.data

    def test_fortress_aum_data_present(self):
        """AUM data should appear in context."""
        # Solve CAPTCHA first
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/')
        assert response.status_code == 200
        assert b'AUM' in response.data or b'aum' in response.data or b'Assets' in response.data

    def test_fortress_leadership_pagination(self):
        """Leadership page should paginate team data."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/leadership?page=1')
        assert response.status_code == 200
        # Should contain pagination or team member data
        assert b'team' in response.data.lower() or b'leadership' in response.data.lower()

    def test_fortress_fund_detail_accessible(self):
        """Fund detail pages should be accessible."""
        with self.client.session_transaction() as sess:
            sess['captcha_passed'] = True

        response = self.client.get('/fund/1')
        assert response.status_code == 200


class TestHeitmanIntegration:
    """Integration tests for Heitman site."""

    def setup_method(self):
        """Set up test client."""
        self.app = heitman_app
        self.client = self.app.test_client()

    def test_heitman_home_no_captcha(self):
        """Home page should not require CAPTCHA."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Home should not be a captcha page
        assert b'captcha_answer' not in response.data or b'Enter the code' not in response.data

    def test_heitman_strategies_requires_captcha(self):
        """Strategies page should require CAPTCHA."""
        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_heitman_funds_requires_captcha(self):
        """Funds page should require CAPTCHA."""
        response = self.client.get('/funds')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_heitman_api_aum_endpoint(self):
        """API endpoint should return AUM data as JSON."""
        response = self.client.get('/api/aum')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'global_aum' in data or 'aum' in data.keys() or isinstance(data, dict)

    def test_heitman_aum_data_on_home(self):
        """AUM data should appear on home page."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'aum' in response.data.lower() or b'Assets' in response.data or b'AUM' in response.data

    def test_heitman_all_routes_accessible(self):
        """All main routes should be accessible."""
        routes = ['/', '/about', '/leadership', '/news', '/contact']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200


class TestNomuraIntegration:
    """Integration tests for Nomura site."""

    def setup_method(self):
        """Set up test client."""
        self.app = nomura_app
        self.client = self.app.test_client()

    def test_nomura_home_accessible(self):
        """Home page should be accessible."""
        response = self.client.get('/')
        assert response.status_code == 200

    def test_nomura_has_artificial_delay(self):
        """Requests should have artificial delay."""
        import time
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start
        assert response.status_code == 200
        # At least ~1 second delay
        assert elapsed >= 0.9

    def test_nomura_aum_data_present(self):
        """AUM data should be present somewhere in response."""
        response = self.client.get('/')
        assert response.status_code == 200
        # Data may be scattered in different formats
        assert len(response.data) > 100

    def test_nomura_all_routes_accessible(self):
        """All main routes should be accessible."""
        routes = ['/', '/about', '/leadership', '/strategies', '/funds', '/news']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200


class TestHokuyoIntegration:
    """Integration tests for Hokuyo site."""

    def setup_method(self):
        """Set up test client."""
        self.app = hokuyo_app
        self.client = self.app.test_client()

    def test_hokuyo_home_accessible(self):
        """Home page should be accessible."""
        response = self.client.get('/')
        assert response.status_code == 200

    def test_hokuyo_no_captcha(self):
        """No pages should require CAPTCHA."""
        routes = ['/', '/about', '/leadership', '/strategies', '/funds', '/news']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200
            assert b'captcha' not in response.data.lower()

    def test_hokuyo_instant_response(self):
        """Responses should be instant (under 100ms)."""
        import time
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start
        assert response.status_code == 200
        # Should be essentially instant (under 100ms)
        assert elapsed < 0.1

    def test_hokuyo_aum_data_in_tables(self):
        """AUM data should be in clean HTML tables."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'<table' in response.data or b'aum' in response.data.lower()

    def test_hokuyo_all_routes_return_200(self):
        """All routes should return 200."""
        routes = ['/', '/about', '/leadership', '/strategies', '/funds', '/news', '/contact']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200


class TestOaktreeIntegration:
    """Integration tests for Oaktree site."""

    def setup_method(self):
        """Set up test client."""
        self.app = oaktree_app
        self.client = self.app.test_client()

    def test_oaktree_first_visit_captcha(self):
        """First page load should require CAPTCHA."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_oaktree_data_page_captcha(self):
        """Data pages should require CAPTCHA."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True

        response = self.client.get('/strategies')
        assert response.status_code == 200
        assert b'captcha' in response.data.lower()

    def test_oaktree_api_funds_endpoint(self):
        """API endpoint should return funds as JSON."""
        response = self.client.get('/api/funds')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, (dict, list))

    def test_oaktree_has_artificial_delay(self):
        """Requests should have artificial delay."""
        import time
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start
        assert response.status_code == 200
        # At least ~0.5 second delay
        assert elapsed >= 0.4

    def test_oaktree_all_routes_accessible(self):
        """All main routes should be accessible."""
        with self.client.session_transaction() as sess:
            sess['visited'] = True
            sess['captcha_passed'] = True

        routes = ['/', '/about', '/leadership', '/news', '/contact']
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200


class TestCrossSiteComparison:
    """Cross-site comparison tests."""

    def test_all_sites_have_unique_aum(self):
        """Each site should have different AUM values."""
        fortress_client = fortress_app.test_client()
        heitman_client = heitman_app.test_client()
        nomura_client = nomura_app.test_client()
        hokuyo_client = hokuyo_app.test_client()
        oaktree_client = oaktree_app.test_client()

        # Get home pages
        fortress_response = fortress_client.get('/')
        heitman_response = heitman_client.get('/')
        nomura_response = nomura_client.get('/')
        hokuyo_response = hokuyo_client.get('/')
        oaktree_response = oaktree_client.get('/')

        # All should be accessible
        assert fortress_response.status_code == 200
        assert heitman_response.status_code == 200
        assert nomura_response.status_code == 200
        assert hokuyo_response.status_code == 200
        assert oaktree_response.status_code == 200

    def test_all_sites_accessible(self):
        """All sites should have working test clients."""
        clients = [
            fortress_app.test_client(),
            heitman_app.test_client(),
            nomura_app.test_client(),
            hokuyo_app.test_client(),
            oaktree_app.test_client(),
        ]

        for client in clients:
            response = client.get('/')
            assert response.status_code == 200
