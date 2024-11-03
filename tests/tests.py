import pytest
from mailbox_org_api import APIClient

def test_headers():
    client = APIClient.APIClient()
    assert client.auth_id is None
    assert client.level is None
    assert client.jsonrpc_id == 0

def test_hello_world():
    client = APIClient.APIClient()
    assert client.jsonrpc_id == 0
    assert client.hello_world() == 'Hello World!'
    assert client.jsonrpc_id == 1