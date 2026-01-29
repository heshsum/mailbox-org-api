from mailbox_org_api import APIClient
from mailbox_org_api.APIError import APIError
import unittest
import os
import time
import secrets
import string

api_test_user = os.environ['API_TEST_USER']
api_test_pass = os.environ['API_TEST_PASS']

# Create a unique ID String by using the Unix time,
# converted to int (to get rid of the decimal) and then to String
test_id = str(int(time.time()))

def generate_pw():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(42))
    return password

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
        api.deauth()

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
        api.deauth()

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
        api.deauth()

    def test_account_set(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        api.account_set(api_test_user, memo=test_id)
        self.assertEqual(api.account_get(api_test_user)['memo'], test_id)

        test_id2 = str(int(time.time()))
        api.account_set(api_test_user, memo=test_id2)
        self.assertEqual(api.account_get(api_test_user)['memo'], test_id2)
        api.deauth()

    def test_account_invoice_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_list(api_test_user)
        for invoice in invoices:
            self.assertTrue(str.startswith(invoice['invoiceNumber'], 'BMBO-'))
        self.assertEqual('2025-10-30', invoices[0]['date'])
        self.assertEqual(0, invoices[0]['amount'])
        self.assertEqual('invoice', invoices[0]['paymentType'])
        self.assertEqual('storniert', invoices[0]['status'])
        self.assertEqual(['csv', 'pdf', 'xml'], invoices[0]['availableDownloadFileTypes'])
        self.assertEqual('BMBO-83002-25', invoices[0]['invoice_id'])
        self.assertIsNotNone(invoices[0]['token'])
        api.deauth()

    def test_account_invoice_get_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_get_list(api_test_user)
        self.assertIsNotNone(invoices)
        for invoice in invoices:
            self.assertTrue(str.startswith(invoice, 'BMBO-'))
        api.deauth()

    def test_domain_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domains = api.domain_list(api_test_user)
        for domain in domains:
            self.assertIsNotNone(domain['domain'], domain['count_mails'])
            self.assertIsInstance(domain['domain'], str)
            self.assertIsInstance(domain['count_mails'], int)
        api.deauth()

    def test_domain_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domains = api.domain_list(api_test_user)
        self.assertEqual('testbmboapi.internal', domains[0]['domain'])
        self.assertIsNotNone(domains[0]['count_mails'])
        api.deauth()

    def test_mail_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        self.assertIsNotNone(mails)
        self.assertIsNotNone(mails[0]['mail'])
        self.assertIn('@' + domain, mails[0]['mail'])
        self.assertEqual(mails[0]['parent_uid'], api_test_user)
        self.assertIsNotNone(mails[0]['domain'])
        self.assertIsNotNone(mails[0]['type'])
        self.assertIsNotNone(mails[0]['memo'])
        self.assertIsNotNone(mails[0]['forwards'])
        self.assertIsNotNone(mails[0]['aliases'])
        self.assertIsNotNone(mails[0]['capabilities'])
        self.assertEqual(['MAIL_BLACKLIST', 'MAIL_SPAMPROTECTION', 'MAIL_PASSWORDRESET_SMS', 'MAIL_BACKUPRECOVER'],
                         mails[0]['possible_capabilities'])
        self.assertIn(mails[0]['plan'], ['premium', 'standard', 'light'])
        self.assertIsNotNone(mails[0]['creation_date'])
        api.deauth()

    def test_mail_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        mail = mails[0]
        self.assertIn('@' + domain, mail['mail'])
        self.assertEqual(api_test_user, mail['parent_uid'])
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
        api.deauth()

    def test_mail_add(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)

        domain = api.domain_list(api_test_user)[0]['domain']
        mail_address = test_id + '@' + domain

        api.mail_add(mail_address, generate_pw(), 'standard', test_id, test_id)
        self.assertEqual(api.mail_get(mail_address)['mail'], mail_address)

    def test_mail_externaluid(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        mail = mails[0]['mail']

        # Setting the external uid
        api.mail_set(mail, uid_extern=test_id)
        returned_mail = api.mail_externaluid(api_test_user, test_id)

        self.assertEqual(returned_mail['mail'], mail)
        api.deauth()

    def test_mail_set(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mail = test_id + '@' + domain

        self.assertRaises(Exception, api.mail_set(mail, password=generate_pw(), password_hash='123'))

        mail_set_tests = {'same_password_allowed': True, 'require_reset_password': True,
                          'plan': 'premium', 'additional_mail_quota': '5', 'additional_cloud_quota': 5,
                          'first_name': test_id, 'last_name': test_id, 'inboxsave': True,
                          'forwards': [test_id + '_forward@' + domain], 'aliases': [test_id + '_alias@' + domain],
                          'alternate_mail': test_id + '_alternate@' + domain, 'memo': 'memo_string',
                          'active': True, 'title': 'Title', 'position': 'Job Position', 'department': 'Department',
                          'company': 'Company', 'street': 'Street 1', 'postal_code': '12345', 'city': 'City',
                          'uid_extern': 'uidextern', 'language': 'de_DE'}

        for k, v in mail_set_tests.items():
            self.assertEqual(api.mail_set(mail, k=v), api.mail_get(mail)[k])
        api.deauth()


    def test_mail_set_state(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        mail = mails[0]['mail']

        api.mail_set_state(mail, False)
        self.assertEqual(api.mail_get(mail)['active'], False)
        api.mail_set_state(mail, True)
        self.assertEqual(api.mail_get(mail)['active'], True)
        api.deauth()

    def test_mail_set_plan(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domain = api.domain_list(api_test_user)[0]['domain']
        mails = api.mail_list(domain)
        mail = mails[0]['mail']
        plans = ['light', 'standard', 'premium']
        for plan in plans:
            api.mail_set_plan(mail, plan)
            self.assertEqual(str(api.mail_get(mail)['plan']).lower(), plan)
        api.deauth()

