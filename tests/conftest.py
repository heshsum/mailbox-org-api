import os
import pytest

from mailbox_org_api import APIClient


@pytest.fixture
def api_client():
    """
    Fixture providing an authenticated APIClient instance.
    Automatically deauthenticates upon test completion.
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


@pytest.fixture
def api(api_client):
    """Alias for api_client fixture."""
    return api_client


@pytest.fixture
def domain(api_client):
    """
    Fixture providing the first domain associated with the test account.
    """
    user = os.environ['API_TEST_USER']
    return api_client.domain_list(user)[0]['domain']
