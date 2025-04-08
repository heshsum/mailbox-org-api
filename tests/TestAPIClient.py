from mailbox_org_api import APIClient
import unittest

class TestAPIClient(unittest.TestCase):
    def test_headers(self):
        client = APIClient.APIClient()
        self.assertEqual(client.auth_id, None)
        self.assertEqual(client.level, None)
        self.assertEqual(client.jsonrpc_id, 0)

    def test_hello_world(self):
        client = APIClient.APIClient()
        self.assertEqual(client.jsonrpc_id, 0)
        self.assertEqual(client.hello_world(), 'Hello World!')
        self.assertEqual(client.jsonrpc_id, 1)