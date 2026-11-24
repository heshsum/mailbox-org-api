import os
import re
import time
from importlib.metadata import version

import pytest

from mailbox_org_api import APIClient

# Mailboxes created by test runs are named '<API_TEST_ID>@<domain>', where API_TEST_ID is a Unix timestamp
stray_mailbox_pattern = re.compile(r'^(\d{10})@')

# Only mailboxes older than this are deleted, so a test run running at the same time (e.g. locally and on
# GitHub Actions) doesn't lose its mailbox. A complete test run takes less than two minutes.
stray_mailbox_min_age = 60 * 60


def pytest_configure(config):
    """
    Create one unique ID per test run for objects created on the live API.
    It is set in the main process before pytest-xdist spawns its workers, so all workers share the same ID.
    """
    os.environ.setdefault('API_TEST_ID', str(int(time.time())))


def pytest_sessionstart(session):
    """
    Delete stray mailboxes of earlier test runs before the tests start.
    Mailboxes are left behind if a test run is aborted before the mail_cleanup fixture runs.
    Runs once in the main process only, not in each pytest-xdist worker.
    """
    if hasattr(session.config, 'workerinput'):
        return
    reporter = session.config.pluginmanager.get_plugin('terminalreporter')

    def report(line):
        if reporter is not None:
            reporter.write_line(line)

    try:
        user = os.environ['API_TEST_USER']
        with APIClient.APIClient() as api:
            api.auth(user, os.environ['API_TEST_PASS'])
            domain = api.domain_list(user)[0]['domain']
            now = int(time.time())
            for mail in api.mail_get_list(domain):
                match = stray_mailbox_pattern.match(mail)
                if not match or now - int(match.group(1)) < stray_mailbox_min_age:
                    continue
                try:
                    api.mail_del(mail)
                    report(f'Deleted stray test mailbox {mail}')
                except Exception as error:
                    report(f'Could not delete stray test mailbox {mail}: {error}')
    except Exception as error:
        # A failed cleanup must not prevent the test run
        report(f'Cleanup of stray test mailboxes failed: {error}')


def pytest_runtest_setup(item):
    """
    Fail grouped tests if pytest-xdist did not apply the xdist groups with --dist=loadgroup.
    Otherwise tests depending on each other run on different workers and are silently skipped.
    pytest-xdist marks grouped tests by appending '@<group>' to the node ID, which pytest 9.2 no longer allows.
    """
    config = item.config
    if (hasattr(config, 'workerinput') and config.getvalue('loadgroup')
            and item.get_closest_marker('xdist_group') and '@' not in item.nodeid):
        pytest.fail(f'xdist group not applied by pytest-xdist {version("pytest-xdist")} '
                    f'with pytest {pytest.__version__}. Run without -n or use a supported pytest version.',
                    pytrace=False)


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
