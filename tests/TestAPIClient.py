from mailbox_org_api import APIClient
from mailbox_org_api.APIError import APIError
import unittest
import os

api_test_user = os.environ['API_TEST_USER']
api_test_pass = os.environ['API_TEST_PASS']

class TestAPIClient(unittest.TestCase):
    def test_headers(self):
        api = APIClient.APIClient()
        self.assertEqual(api.auth_id, None)
        self.assertEqual(api.level, None)
        self.assertEqual(api.jsonrpc_id, 0)

    #def test_hello_world(self):
    #    api = APIClient.APIClient()
    #    self.assertEqual(api.jsonrpc_id, 0)
    #    self.assertEqual(api.hello_world(), 'Hello World!')
    #    self.assertEqual(api.jsonrpc_id, 1)

    def test_API_error(self):
        api = APIClient.APIClient()
        with self.assertRaises(APIError):
            api.auth('wröng_üser?', 'wröng_pässwörd!')
