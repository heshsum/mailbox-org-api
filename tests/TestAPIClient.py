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

    def test_login(self):
        api = APIClient.APIClient()
        self.assertEqual(api.jsonrpc_id, 0)
        api.auth(api_test_user, api_test_pass)
        self.assertNotEqual(api.auth_id, None)
        self.assertEqual(api.level, 'account')
        self.assertEqual(api.jsonrpc_id, 1)

    def test_account_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        account = api.account_get(api_test_user)
        self.assertEqual('test_bmbo_api', account['account'])
        self.assertEqual(account['type'], 'BMBO')
        self.assertEqual(account['status'], 'aktiv')
        self.assertEqual(account['language'], 'de_DE')
        self.assertEqual(account['plan'], 'basic')
        self.assertEqual(account['company'], 'test_bmbo_api')
        self.assertEqual(account['ustid'], 'DE1234567')

    def test_account_get_object(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        account = api.account_get_object(api_test_user)
        self.assertEqual(account.account, 'test_bmbo_api')
        self.assertEqual(account.type, 'BMBO')
        self.assertEqual(account.status, 'aktiv')
        self.assertEqual(account.language, 'de_DE')
        self.assertEqual(account.plan, 'basic')
        self.assertEqual(account.company, 'test_bmbo_api')
        self.assertEqual(account.ustid, 'DE1234567')

    def test_account_invoice_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_list(api_test_user)
        self.assertEqual(2, len(invoices))
        self.assertEqual('BMBO-83002-25', invoices[0]['invoiceNumber'])
        self.assertEqual('2025-10-30', invoices[0]['date'])
        self.assertEqual(0, invoices[0]['amount'])
        self.assertEqual('invoice', invoices[0]['paymentType'])
        self.assertEqual('storniert', invoices[0]['status'])
        self.assertEqual(['csv', 'pdf', 'xml'], invoices[0]['availableDownloadFileTypes'])
        self.assertEqual('BMBO-83002-25', invoices[0]['invoice_id'])
        self.assertIsNotNone(invoices[0]['token'])

    def test_domain_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        self.assertGreater(len(api.domain_list(api_test_user)), 0)

    def test_domain_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domains = api.domain_list(api_test_user)
        self.assertEqual('testbmboapi.internal', domains[0]['domain'])
        self.assertIsNotNone(domains[0]['count_mails'])

    def test_mail_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        self.assertGreater(len(mails), 0)

    def test_mail_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        mail = mails[0]
        self.assertIn('@' + domain, mail['mail'])
        self.assertIn(api_test_user, mail['parent_uid'])
        self.assertIn(domain, mail['domain'])
        self.assertIn('inbox', mail['type'])
        self.assertIsNotNone(mail['memo'])
        self.assertIsNotNone(mail['forwards'])
        self.assertIsNotNone(mail['aliases'])
        self.assertIsNotNone(mail['capabilities'])
        self.assertEqual(['MAIL_BLACKLIST', 'MAIL_SPAMPROTECTION', 'MAIL_PASSWORDRESET_SMS', 'MAIL_BACKUPRECOVER'],
                         mail['possible_capabilities'])
        self.assertIn(mail['plan'], ['premium', 'standard', 'light'])
        self.assertIsNotNone(mail['creation_date'])

