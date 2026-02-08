from mailbox_org_api import APIClient
from mailbox_org_api.APIError import APIError
import pytest
import os
import time
import secrets
import string

api_test_user = os.environ['API_TEST_USER']
api_test_pass = os.environ['API_TEST_PASS']

# Create a unique ID String by using the Unix time,
# converted to int (to get rid of the decimal) and then to String
def generate_id():
    return str(int(time.time()))

def generate_pw():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(42))
    return password

def get_domain():
    api = APIClient.APIClient()
    api.auth(api_test_user, api_test_pass)
    domain = api.domain_list(api_test_user)[0]['domain']
    api.deauth()
    return domain

test_id = generate_id()
domain = get_domain()

class TestAPIClient:
    def test_validate_params(self):
        allowed = {'string': str}
        with pytest.raises(ValueError):
            APIClient.validate_params(allowed, {'integer':123})
        with pytest.raises(TypeError):
            APIClient.validate_params(allowed, {'string':123})

    def test_headers(self):
        api = APIClient.APIClient()
        assert api.auth_id is None
        assert api.level is None
        assert api.jsonrpc_id is 0

    def test_hello_world(self):
        api = APIClient.APIClient()
        assert api.jsonrpc_id == 0
        assert api.hello_world() == 'Hello World!'
        assert api.jsonrpc_id == 1

    def test_API_error(self):
        api = APIClient.APIClient()
        with pytest.raises(APIError):
            api.auth('wröng_üser?', 'wröng_pässwörd!')

    def test_login(self):
        api = APIClient.APIClient()
        assert api.jsonrpc_id == 0
        api.auth(api_test_user, api_test_pass)
        assert api.auth_id is not None
        assert api.level == 'account'
        assert api.jsonrpc_id == 1
        api.deauth()

    def test_account_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        account = api.account_get(api_test_user)
        assert account['account'] == 'test_bmbo_api'
        assert account['type'] == 'BMBO'
        assert account['status'] == 'aktiv'
        assert account['language'] == 'de_DE'
        assert account['plan'] == 'basic'
        assert account['company'] == 'test_bmbo_api'
        assert account['ustid'] == 'DE1234567'
        api.deauth()

    def test_account_get_object(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        account = api.account_get_object(api_test_user)
        assert account.account == 'test_bmbo_api'
        assert account.type == 'BMBO'
        assert account.status == 'aktiv'
        assert account.language == 'de_DE'
        assert account.plan == 'basic'
        assert account.company == 'test_bmbo_api'
        assert account.ustid == 'DE1234567'
        api.deauth()

    def test_account_set(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        api.account_set(api_test_user, memo=test_id)
        assert api.account_get(api_test_user)['memo'] == test_id

        test_id2 = str(int(time.time()))
        api.account_set(api_test_user, memo=test_id2)
        assert api.account_get(api_test_user)['memo'] == test_id2
        api.deauth()

    def test_account_invoice_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_list(api_test_user)
        for invoice in invoices:
            assert str.startswith(invoice['invoiceNumber'], 'BMBO-')
        assert invoices[0]['date'] == '2025-10-30'
        assert invoices[0]['amount'] == 0
        assert invoices[0]['paymentType'] == 'invoice'
        assert invoices[0]['status'] == 'storniert'
        assert invoices[0]['availableDownloadFileTypes'] == ['csv', 'pdf', 'xml']
        assert invoices[0]['invoice_id'] == 'BMBO-83002-25'
        assert invoices[0]['token'] is not None
        api.deauth()

    def test_account_invoice_get_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_get_list(api_test_user)
        assert invoices is not None
        for invoice in invoices:
            assert str.startswith(invoice, 'BMBO-')
        api.deauth()

    def test_account_invoice_list_open(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_get_list_open(api_test_user)
        assert invoices is not None
        # The test account does not have any open invoices
        assert len(invoices) == 0
        api.deauth()

    def test_account_invoice_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_list(api_test_user)
        invoice = api.account_invoice_get(api_test_user, invoices[0]['token'])
        assert invoices[0]['invoice_id'] in str(invoice)
        api.deauth()

    def test_account_invoice_get_object(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoices = api.account_invoice_list(api_test_user)
        invoice = api.account_invoice_get_object(api_test_user, invoices[0]['invoice_id'])
        assert invoice.invoice_id == invoices[0]['invoice_id']
        assert invoice.status == invoices[0]['status']
        assert invoice.account == api_test_user
        assert invoice.token is not None
        assert invoice.date == invoices[0]['date']
        api.deauth()

    def test_account_invoice_get_file(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoice = api.account_invoice_get_list(api_test_user)[0]
        csv = api.account_invoice_get_file(api_test_user, invoice, 'csv')
        assert 'date,services,description,quantity,currency,net,vat_percent,total' in str(csv)
        pdf = api.account_invoice_get_file(api_test_user, invoice, 'pdf')
        assert 'PDF-1.7' in str(pdf)
        xml = api.account_invoice_get_file(api_test_user, invoice, 'xml')
        assert 'xml version="1.0" encoding="UTF-8"' in str(xml)
        api.deauth()

    def test_account_invoice_get_token(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        invoice = api.account_invoice_get_list(api_test_user)[0]
        token = api.account_invoice_get_token(api_test_user, invoice_id=invoice)
        assert len(token) >0
        assert isinstance(token, str)
        api.deauth()

    def test_domain_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domains = api.domain_list(api_test_user)
        for d in domains:
            assert d['domain'] is not None
            assert d['count_mails'] is not None
            assert isinstance(d['domain'], str)
            assert isinstance(d['count_mails'], int)
        api.deauth()

    def test_domain_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        domains = api.domain_list(api_test_user)
        assert domains[0]['count_mails'] is not None
        api.deauth()

    def test_domain_set(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        api.domain_set(domain, memo=test_id)
        assert api.domain_get(domain)['memo'] == test_id

    def test_domain_capabilities_set(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        api.domain_capabilities_set(domain, ['MAIL_SPAMPROTECTION'])
        for m in api.mail_list(domain):
            assert m['capabilities'] == ['MAIL_SPAMPROTECTION']
        api.domain_capabilities_set(domain, [])
        for m in api.mail_list(domain):
            assert m['capabilities'] == []

    def test_mail_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mails = api.mail_list(domain)
        assert mails is not None
        assert mails[0]['mail'] is not None
        assert '@' in mails[0]['mail'] and domain in mails[0]['mail']
        assert mails[0]['parent_uid'] == api_test_user
        assert mails[0]['domain'] is not None
        assert mails[0]['type'] is not None
        assert mails[0]['memo'] is not None
        assert mails[0]['forwards'] is not None
        assert mails[0]['aliases'] is not None
        assert mails[0]['capabilities'] is not None
        assert (mails[0]['possible_capabilities'] ==
                ['MAIL_BLACKLIST', 'MAIL_SPAMPROTECTION', 'MAIL_PASSWORDRESET_SMS', 'MAIL_BACKUPRECOVER'])
        assert mails[0]['plan'] in ['premium', 'standard', 'light']
        assert mails[0]['creation_date'] is not None
        with pytest.raises(APIError):
            api.mail_list(domain, page = 2)
        with pytest.raises(APIError):
            api.mail_list(domain, page_size=-1)
        with pytest.raises(ValueError):
            api.mail_list(domain, sort_order='wröng')
        api.deauth()

    def test_mail_get(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mails = api.mail_list(domain)
        mail = mails[0]
        assert '@' in mail['mail'] and domain in mail['mail']
        assert mail['parent_uid'] == api_test_user
        assert mail['domain'] == domain
        assert mail['type'] in ['inbox', 'inboxforward', 'forward']
        assert mail['memo'] is not None
        assert mail['forwards'] is not None
        assert mail['aliases'] is not None
        assert mail['capabilities'] is not None
        assert (mail['possible_capabilities'] ==
                ['MAIL_BLACKLIST', 'MAIL_SPAMPROTECTION', 'MAIL_PASSWORDRESET_SMS', 'MAIL_BACKUPRECOVER'])
        assert mail['plan'] in ['premium', 'standard', 'light']
        assert mail['creation_date'] is not None
        api.deauth()

    def test_mail_add(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)

        mail_address = test_id + '@' + domain

        api.mail_add(mail_address, generate_pw(), 'standard', test_id, test_id)
        assert api.mail_get(mail_address)['mail'] == mail_address
        api.deauth()

    def test_mail_externaluid(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mails = api.mail_list(domain)
        mail = mails[0]['mail']

        # Setting the external uid
        api.mail_set(mail, uid_extern=test_id)
        returned_mail = api.mail_externaluid(api_test_user, test_id)

        assert returned_mail['mail'] == mail
        api.deauth()

    @pytest.mark.depends(name=['test_mail_add'])
    def test_mail_set(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain

        # Defining parameters and their values to test
        mail_set_tests = {'require_reset_password': True, 'plan': 'premium', 'first_name': test_id,
                          'last_name': test_id, 'inboxsave': True, 'forwards': [test_id + '_forward@' + domain],
                          'aliases': [test_id + '_alias@' + domain], 'alternate_mail': test_id + '_alternate@' + domain,
                          'memo': 'memo_string', 'active': True, 'title': 'Title', 'position': 'Job Position',
                          'department': 'Department', 'company': 'Company', 'street': 'Street 1',
                          'postal_code': '12345', 'city': 'City', 'phone':'+492345678', 'fax':'+492345678',
                          'cell_phone':'+492345678', 'uid_extern': generate_pw(), 'language': 'de_DE'}

        # Adding parameters to call
        params = {}
        params.update({k: v for k, v in mail_set_tests.items()})
        api.mail_set(mail, **params)

        # Getting mail from API to act as the reference
        check_mail = api.mail_get(mail)

        # Compare values sent to values received
        for k, v in mail_set_tests.items():
            assert check_mail[k] == v

        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_capabilities_set(self):
        capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST', 'MAIL_BACKUPRECOVER', 'MAIL_PASSWORDRESET_SMS']

        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        for i in capabilities:
            api.mail_capabilities_set(mail, [i])
            # The API returns a list of capabilities
            capabilities = api.mail_get(mail)['capabilities']
            assert len(capabilities) == 1
            assert i in capabilities
        api.mail_capabilities_set(mail, [])
        assert api.mail_get(mail)['capabilities'] == []
        api.deauth()

    def test_mail_set_state(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mails = api.mail_list(domain)
        mail = mails[0]['mail']

        api.mail_set_state(mail, False)
        assert api.mail_get(mail)['active'] == False
        api.mail_set_state(mail, True)
        assert api.mail_get(mail)['active'] == True
        api.deauth()

    def test_mail_set_plan(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mails = api.mail_list(domain)
        mail = mails[0]['mail']
        plans = ['standard', 'premium']
        for plan in plans:
            api.mail_set_plan(mail, plan)
            assert str(api.mail_get(mail)['plan']).lower() == plan
        with pytest.raises(APIError):
            api.mail_set_plan(mail, 'light')
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_set_aliases(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        aliases = []
        api.mail_set_aliases(mail, aliases)
        for i in range(0, 5):
            address = test_id + '_alias_' + str(i) + '@' + domain
            aliases.append(address)
        api.mail_set_aliases(mail, aliases)
        assert api.mail_get(mail)['aliases'] == aliases
        api.mail_set_aliases(mail, [])
        assert api.mail_get(mail)['aliases'] == []
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_set_forwards(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        forwards = []
        api.mail_set_forwards(mail, forwards)
        for i in range(4):
            address = test_id + '_forward_' + str(i) + '@' + domain
            forwards.append(address)
        api.mail_set_forwards(mail, forwards)
        assert api.mail_get(mail)['forwards'] == forwards
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_set_password(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        # Set a newly generated password
        # As the response is just the mailbox info, the assertion is a comparison with mail_get
        assert api.mail_set_password(mail, generate_pw()) == api.mail_get(mail)
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_set_password_require_reset(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        # Set a newly generated password
        # As the response is just the mailbox info, the assertion is a comparison with mail_get
        assert api.mail_set_password_require_reset(mail, generate_pw()) == api.mail_get(mail)
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_apppassword_add(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        len_before = len(api.mail_apppassword_list(mail))
        api.mail_apppassword_add(mail, test_id, True, True)
        assert len(api.mail_apppassword_list(mail)) == len_before + 1
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    def test_mail_apppassword_list(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        assert len(api.mail_apppassword_list(mail)) > 0
        api.deauth()

    @pytest.mark.depends(name=["test_mail_add"])
    @pytest.mark.depends(name=['test_mail_apppassword_add'])
    @pytest.mark.depends(name=['test_mail_apppassword_list'])
    def test_mail_apppassword_del(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain

        app_passwords = api.mail_apppassword_list(mail)
        assert len(app_passwords) > 0

        # Delete all app passwords
        for i in app_passwords:
            api.mail_apppassword_del(i['id'])

        # After deleting all app passwords, length should be 0
        assert len(api.mail_apppassword_list(mail)) == 0

    @pytest.mark.depends(name=['test_mail_add'])
    def test_mail_set_deletion_date(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        deletion_date = '31.12.2099'
        assert deletion_date not in api.mail_get(mail)
        api.mail_set_deletion_date(mail, deletion_date)
        assert deletion_date in api.mail_get(mail)['deletion_date']
        api.deauth()

    @pytest.mark.depends(name=['test_mail_add'])
    def test_search(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain
        assert mail in api.search(mail)['emails']
        assert domain in api.search(domain)['domains']
        assert api_test_user in api.search(api_test_user)['accounts']

    @pytest.mark.order('last')
    def test_mail_del(self):
        api = APIClient.APIClient()
        api.auth(api_test_user, api_test_pass)
        mail = test_id + '@' + domain

        mails = api.mail_list(domain)

        mail_addresses = []
        for i in mails:
            mail_addresses.append(i['mail'])

        assert mail in mail_addresses

        api.mail_del(mail)

        mails = api.mail_list(domain)
        mail_addresses = []
        for i in mails:
            mail_addresses.append(i['mail'])
        assert mail not in mail_addresses
        api.deauth()
