import pytest
from webtest import TestApp
from werkzeug.exceptions import abort

from app.main import app as _app


# Create a route specifically for testing 500 errors
@_app.route('/fivehundred')
def fivehundred():
    abort(500)


@pytest.fixture
def app_config():
    settings = {
        'TESTING': True,
        'DEBUG': True,
        'SECRET_KEY': 'a key for testing',
        'WTF_CSRF_ENABLED': False,
    }
    return settings


@pytest.fixture
def app(app_config):
    _app.config.update(app_config)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def test_client(app):
    """
    Configure a WebTest client for nice convenience methods."""
    return TestApp(app)

