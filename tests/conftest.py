import os
import time
import pytest

from mailbox_org_api import APIClient


def pytest_configure(config):
    """
    Create one unique ID per test run for objects created on the live API.
    It is set in the main process before pytest-xdist spawns its workers, so all workers share the same ID.
    """
    os.environ.setdefault('API_TEST_ID', str(int(time.time())))


@pytest.fixture(scope='session')
def api_client():
    """
    Fixture providing an authenticated APIClient instance.
    Authenticates once per test session and deauthenticates at the end.
    """
    user = os.environ['API_TEST_USER']
    password = os.environ['API_TEST_PASS']
    client = APIClient.APIClient()
    client.auth(user, password)
    try:
        yield client
    finally:
        try:
            client.deauth()
        except Exception:
            pass


@pytest.fixture(scope='session')
def api(api_client):
    """Alias for api_client fixture."""
    return api_client


@pytest.fixture(scope='session')
def domain(api_client):
    """
    Fixture providing the first domain associated with the test account.
    """
    user = os.environ['API_TEST_USER']
    return api_client.domain_list(user)[0]['domain']
