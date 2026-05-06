import pytest
from flask import session
from utils.dom_obfuscator import generate_class_map

# Create a minimal Flask app for testing
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key'


def test_generate_class_map_creates_random_strings():
    """Test that class map generates 5-char random strings."""
    with app.test_request_context():
        result = generate_class_map(session)
        assert isinstance(result, dict)
        assert 'aum-value' in result
        assert len(result['aum-value']) == 5
        assert result['aum-value'].isalnum()


def test_generate_class_map_returns_existing():
    """Test that existing map is returned unchanged."""
    with app.test_request_context():
        result1 = generate_class_map(session)
        result2 = generate_class_map(session)
        assert result1 == result2
