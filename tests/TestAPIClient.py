from mailbox_org_api import APIClient
from mailbox_org_api.APIError import APIError
import unittest
import os

api_test_user = os.environ['API_TEST_USER']
api_test_pass = os.environ['API_TEST_PASS']

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

    def test_API_error(self):
        client = APIClient.APIClient()
        with self.assertRaises(APIError):
            client.auth('wröng_üser?', 'wröng_pässwörd!')