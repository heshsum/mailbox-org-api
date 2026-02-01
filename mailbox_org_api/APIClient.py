"""
Module for the mailbox Business API client
"""
import json
from warnings import deprecated
import requests
from requests import RequestException

from mailbox_org_api.APIError import APIError
from mailbox_org_api.Account import Account
from mailbox_org_api.Mail import Mail
from mailbox_org_api.Invoice import Invoice

headers = {'content-type': 'application/json'}

# Domain capabilities as documented here: https://api.mailbox.org/v1/doc/methods/index.html#domain-capabilities-set
domain_capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST', 'MAIL_BACKUPRECOVER', 'MAIL_PASSWORDRESET_SMS']

# Capabilities as documented here: https://api.mailbox.org/v1/doc/methods/index.html#mail-capabilities-set
mail_capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST', 'MAIL_BACKUPRECOVER', 'MAIL_OTP', 'MAIL_PASSWORDRESET_SMS']

# Allowed sort fields as documented here: https://api.mailbox.org/v1/doc/methods/index.html#mail-list
mail_list_sort_field = ['mail', 'first_name', 'last_name', 'status', 'domain', 'plan', 'type', 'creation_date']

# Allowed attributes as documented here: https://api.mailbox.org/v1/doc/methods/index.html#mail-set
mail_set_attributes = {'password': str, 'password_hash': str, 'same_password_allowed': bool,
                      'require_reset_password': bool, 'plan': str, 'additional_mail_quota': str,
                      'additional_cloud_quota': str, 'first_name': str, 'last_name': str, 'inboxsave': bool,
                      'forwards': list, 'aliases': list, 'alternate_mail': str, 'memo': str, 'allow_nets': str,
                      'active': bool, 'title': str, 'birthday': str, 'position': str, 'department': str, 'company': str,
                      'street': str, 'postal_code': str, 'city': str, 'phone': str, 'fax': str, 'cell_phone': str,
                      'uid_extern': str, 'language': str, 'deletion_date': str}

# Allowed attributes as documented here: https://api.mailbox.org/v1/doc/methods/index.html#account-add
account_add_attributes = {'tarifflimits': dict, 'memo': str, 'contact_mail': str, 'contact_phone': str,
                         'contact_fax': str, 'contact_mobile': str, 'company': str, 'ustid': str,
                         'address_main_salutation': str, 'address_main_first_name': str, 'address_main_last_name': str,
                         'address_main_street': str, 'address_main_zipcode': str, 'address_main_town': str,
                         'address_main_country': str, 'address_payment_same_as_main': bool,
                         'address_payment_first_name': str, 'address_payment_last_name': str,
                         'address_payment_street': str, 'address_payment_zipcode': str, 'address_payment_town': str,
                         'address_payment_country': str, 'max_mailinglist': int, 'language': str}

# Allowed parameters as documented here: https://api.mailbox.org/v1/doc/methods/index.html#account-set
account_set_parameters = {'password': str, 'telephone_password':str, 'plan': str, 'memo': str, 'contact_mail': str,
                          'contact_mail_payment': str, 'contact_phone': str, 'contact_fax': str, 'contact_mobile': str,
                          'address_main_first_name': str, 'address_main_last_name':str, 'address_main_street': str,
                          'address_main_zipcode': str, 'address_main_town': str, 'address_main_country': str,
                          'address_payment_same_as_main': bool, 'address_payment_first_name': str,
                          'address_payment_last_name': str, 'address_payment_company':str,
                          'address_payment_street': str, 'address_payment_zipcode': str, 'address_payment_town': str,
                          'company': str, 'bank_iban': str, 'bank_bic': str, 'bank_account_owner': str,
                          'payment_type':str, 'ustid':str, 'av_contract_accept_name': str, 'max_mailinglist': int,
                          'tarifflimits': list, 'av_contract_professional_secrecy': bool, 'language': str}

class APIClient:
    """
    Object for API Client
    """

    def __init__(self, debug_output=False):
        # URL of the API
        self.url = "https://api.mailbox.org/v1/"

        # JSON RPC ID - a unique ID is required for each request during a session
        self.jsonrpc_id = 0

        # This saves the access level of the user
        self.level = None

        # Session ID when authenticating
        self.auth_id = None

        self.debug_output = debug_output

    # Increment the request ID
    def get_jsonrpc_id(self):
        """Method to create the JSON RPC request ID. """
        self.jsonrpc_id += 1
        return str(self.jsonrpc_id)

    def api_request(self, method: str, params: dict) -> dict:
        """
        Function to send API calls
        :param method: the method to call
        :param params: the parameters to send
        :return: the response from the mailbox.org Business API
        """
        request = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": self.get_jsonrpc_id()
        }
        if self.debug_output:
            # Print the full request but redact sensitive information (passwords).

            # On import copy module if needed
            import copy
            # Create a deep copy of the dict, as not to overwrite information on the original
            print_request = copy.deepcopy(request)

            # Check if any parameter is 'password' or 'pass'.
            # Check explicit for these strings as not to interfere with possible other
            # parameters containing a substring.
            for param in print_request['params']:
                if param == 'password' or param == 'pass':
                    # If True, replace the logged value with 'xxx'
                    print_request['params'][param] = 'xxx'

            # Print the clean version of the request
            print('API full request:\t', print_request)

        api_response = requests.post(
            self.url, data=json.dumps(request), headers=headers)
        try:
            api_response = api_response.json()
        except RequestException as error:
            print('Non-JSON response received.\nFull response:\t', api_response,
                  '\nError:', {error})
        if self.debug_output:
            print('API full response:\t', api_response)

        # Depending on the type of response the return changes.
        # If a successful result, only the result is returned
        if 'result' in api_response:
            if self.debug_output:
                print('API result:\t', api_response['result'])
            return api_response['result']

        # In case of an error, the error is returned
        elif 'error' in api_response:
            error_data = api_response['error']
            raise APIError(message=error_data.get('message'), code=error_data.get('code'))

        # If neither a success nor an error, the full response if returned
        return api_response

    def auth(self, username, password) -> dict:
        """
        Function to authenticate and create a new API session
        :param username: the username
        :param password: the password
        :return: the API response for the request
        """
        api_response = self.api_request('auth', {'user':username, 'pass':password})
        if api_response['session']:
            # Level gives information about the calls available
            self.level = api_response["level"]
            print('Level:', self.level)

            # The session id
            self.auth_id = str(api_response["session"])
            print('Auth ID:', self.auth_id)
            # The auth-header is added to the list of headers, as it has to be provided with each call
            headers.update({"HPLS-AUTH": self.auth_id})
        return api_response

    def deauth(self) -> dict:
        """
        Function to close the current API session
        :return: True if the API session is closed, False otherwise
        """
        api_response = self.api_request('deauth',{})
        if api_response:
            # The auth header is stripped
            del headers["HPLS-AUTH"]
        return api_response

    def hello_world(self):
        """
        Function for hello world, just to test the connection
        :return: The response from the mailbox.org Business API
        """
        return self.api_request('hello.world',{})

    def hello_innerworld(self):
        """
        Hello World function to test the authentication
        :return: The response from the mailbox.org Business API
        """
        return self.api_request('hello.innerworld', {})

    def account_add(self, account: str, password: str, plan: str, **kwargs) -> dict:
        """
        Function to create a new account
        :param account: the account name to create
        :param password: the password of the account
        :param plan: the plan of the account
        :param kwargs: Optional arguments corresponding to API parameters (e.g., payment_type)
                                See API documentation for full list.
        :return: the response from the mailbox.org Business API
        """

        # Check for each argument in kwargs if it is a valid function parameter.
        for arg in kwargs:
            # Check name of argument
            if arg not in account_add_attributes:
                raise ValueError('Parameter', arg, 'not a valid parameter for account_set')

            # Check type for each argument
            if type(kwargs[arg]) != account_add_attributes[arg]:
                raise TypeError('Attribute', arg, 'must be of type', str(account_add_attributes[arg]) + '.',
                                str(type(kwargs[arg])), 'given.')

        # After validation, build parameter list from mail and kwargs
        params = {'account': account, 'password': password, 'plan': plan}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return self.api_request('account.add', params)

    def account_get(self, account: str) -> dict:
        """
        Function to get a specific account
        :param account: the account name to get
        :return: the response from the mailbox.org Business API
        """
        return self.api_request('account.get', {'account':account})

    def account_get_object(self, account:str) -> Account:
        result = self.api_request('account.get', {'account': account})
        account_object = Account(account)
        for k, v in result.items():
            if v:
                setattr(account_object, k, v)
        return account_object

    def account_set(self, account: str, **kwargs) -> dict:
        """
        Function to update a specific account
        :param account: the account name to update
        :param kwargs: Optional arguments corresponding to API parameters (e.g., payment_type)
                                See API documentation for full list.
        :return: the response from the mailbox.org Business API
        """

        # Check for each argument in kwargs if it is a valid function parameter.
        for arg in kwargs:
            # Check name of argument
            if arg not in account_set_parameters:
                raise ValueError('Parameter', arg, 'not a valid parameter for account_set')

            # Check type for each argument
            if type(kwargs[arg]) != account_set_parameters[arg]:
                raise TypeError('Attribute', arg, 'must be of type', str(account_set_parameters[arg]) + '.',
                                str(type(kwargs[arg])), 'given.')

        # After validation, build parameter list from mail and kwargs
        params = {'account': account}
        params.update({k: v for k, v in kwargs.items() if v is not None})

        return self.api_request('account.set', params)

    def account_del(self, account: str) -> dict:
        """
        Function to delete a specific account
        :param account: the account name to delete
        :return: the response from the mailbox.org Business API
        """
        return self.api_request('account.del', {'account':account})

    def account_invoice_list(self, account: str) -> dict:
        """
        Function to list all invoices for a specific account
        :param account: the account name to list
        :return: the response from the mailbox.org Business API
        """
        return self.api_request('account.invoice.list', {'account':account})

    def account_invoice_get(self, account: str, token: str) -> dict:
        """
        Function to get a specific invoice for an account
        :param account: the account name
        :param token: the token for the invoice
        :return: the response from the mailbox.org Business API - the invoice as a Base64 encoded gzipped string
        """
        return self.api_request('account.invoice.get', {'account':account, 'token':token})

    def account_invoice_get_object(self, account: str, invoice_id: str) -> Invoice:
        """
        Function to get a specific invoice object for an account
        :param account: the account name
        :param invoice_id: the id of the invoice to request
        :return: the invoice as an Invoice object
        """
        # Get all invoices for the account
        invoice_list = self.account_invoice_list(account)

        # Initialize the Invoice object
        invoice = Invoice(account, invoice_id)

        # Retrieve the other data for the invoice from the invoice list
        for i in invoice_list:
            if i['invoice_id'] == invoice_id:
                invoice.date = i['date']
                invoice.status = i['status']
                invoice.token = i['token']
        return invoice

    def account_invoice_get_list(self, account: str) -> list:
        """
        Function to get a list of all invoice ids for a specific account
        """
        response = self.api_request('account.invoice.list', {'account':account})
        invoices = []

        for invoice in response:
            invoices.append(invoice['invoice_id'])
        return invoices

    def account_invoice_get_list_open(self, account: str) -> list:
        """
        Function to get a list of all invoice id's with status 'open' for a specific account
        """
        invoices = self.account_invoice_list(account)
        open_invoices = []
        
        for i in invoices:
            if i['status'] == 'open':
                open_invoices.append(i)
        return open_invoices

    def account_invoice_get_token(self, account: str, invoice_id: str) -> str:
        """
        Function to get the token for a specific invoices of an account
        :param account: the account name
        :param invoice_id: the id of the invoice
        :return: the response from the mailbox.org Business API - the token to get the invoice
        """
        response = self.api_request('account.invoice.list', {'account': account})
        for invoice in response:
            if invoice['invoice_id'] == invoice_id:
                return invoice['token']
        raise ValueError('Invoice not found')

    @deprecated('Use account_invoice_get_file instead')
    def account_invoice_get_pdf(self, account: str, invoice_id: str) -> bytes:
        """
        Function to get a specific invoice as a PDf-file
        :param account: the account name
        :param invoice_id: the invoice ID
        :return: the PDF as bytes
        """
        return self.account_invoice_get_file(account, invoice_id, 'pdf')

    def account_invoice_get_file(self, account: str, invoice_id: str, file_type: str) -> bytes:
        """
        Function to get a specific invoice as a PDf-file
        :param account: the account name
        :param invoice_id: the invoice ID
        :param file_type: The file type to return. Valid: csv, pdf and xml
        :return: the file as bytes
        """
        if file_type not in ('csv', 'pdf', 'xml'):
            raise ValueError(file_type, 'is not a valid file type. Valid: csv, pdf and xml')

        import base64
        import zlib

        # Get the token and retrieve the invoice data
        response = self.api_request('account.invoice.get',
                                    {'account': account,
                                     'token': self.account_invoice_get_token(account, invoice_id),
                                     'type': file_type})

        # Take the Base64 encoded data (response['bin']), decode the Base 64, decompress the gz and return the bytes
        return zlib.decompress(base64.b64decode(response['bin']))

    def domain_list(self, account: str) -> dict:
        """
        Function to list all domains
        :param account: the account to list domains for
        :return: the API response
        """
        return self.api_request('domain.list',{'account':account})

    def domain_add(self, account: str, domain: str, password: str) -> dict:
        """
        Function to add a domain
        :param account: the account to add a domain for
        :param domain: the domain to add
        :param password: the password of the domain
        :return: the API response
        """
        return self.api_request('domain.add', {'account':account, 'domain':domain, 'password':password})

    def domain_get(self, domain: str) -> dict:
        """
        Function to get a specific domain
        :param domain: the domain to get
        :return: the API response
        """
        return self.api_request('domain.get',{'domain':domain})

    def domain_capabilities_set(self, domain: str, **kwargs) -> dict:
        """
        Function to set a domain capabilities
        :param domain: the domain to set the capabilities for
        :param kwargs: Optional arguments corresponding to API parameters for capabilities.
                       See API documentation for full list.
        :return: the API response
        """
        for arg in kwargs:
            if arg not in mail_set_attributes:
                raise ValueError('Parameter', arg, 'not a valid parameter for domain_capabilities_set')

            if type(kwargs[arg]) != mail_set_attributes[arg]:
                raise TypeError('Parameter', arg, 'must be of type',
                                str(mail_set_attributes[arg]) + '.', str(type(kwargs[arg])), 'given.')

        # After validation, build parameter list from domain and kwargs
        params = {'domain': domain}
        params.update({k: v for k, v in kwargs.items() if v is not None})

        return self.api_request('domain.capabilities.set', params)

    def domain_set(self, domain: str, attributes: dict) -> dict:
        """
        Function to set a domain
        :param domain: the domain to update
        :param attributes: the attributes to set
        :return:
        """
        params = {'domain':domain }
        for element in attributes:
            params.update({element:attributes[element]})

        return self.api_request('domain.set', params)

    def domain_del(self, account: str, domain: str) -> dict:
        """
        Function to delete a domain
        :param account: the account to delete a domain in
        :param domain: the domain to delete
        :return: the API response
        """
        return self.api_request('domain.del', {'account':account, 'domain':domain})

    def domain_validate_spf(self, domain: str) -> dict:
        """
        Function to validate the SPF entry of a domain
        :param domain: the domain to validate
        :return: the API response - information about the SPF config
        """
        return self.api_request('domain.validate.spf', {'domain':domain})

    def mail_list(self, domain, details: bool = False, page_size: int = -1, page: int = -1, sort_field: str = None,
                  sort_order: str = None) -> dict:
        """
        Function to list all mailboxes
        :param domain: the domain to list
        :param details: whether to show details or not
        :param page_size: Optional pagination. Use value >1 to enable
        :param page: Size of page for pagination. If 'page_size' is used this is mandatory to set >0
        :param sort_field: the field to sort by. Possible values: mail, first_name, last_name, status, domain, plan, type, creation_date
        :param sort_order: the order to sort by. Possible values: 'asc', 'desc'
        :return: the response from the mailbox.org Business API
        """
        params = {'domain':domain, 'details':details}
        if page_size > 0:
            if page < 1:
                raise ValueError('''If 'page_size' is used, a 'page' value > 1 must be specified.''')
            else:
                params.update({'page':page, 'page_size':page_size})
        if sort_field:
            if sort_field not in mail_list_sort_field:
                raise ValueError('Sort field not allowed.')
            else:
                params.update({'sort_field':sort_field})
        if sort_order:
            if sort_order not in ['asc', 'desc']:
                raise ValueError('Sort order must be either "asc" or "desc".')
            else:
                params.update({'sort_order':sort_order})
        return self.api_request('mail.list', params)

    def mail_add(self, mail:str, password: str, plan: str, first_name: str, last_name: str, inboxsave: bool = True,
                 forwards: list = None, memo: str = None, language: str = 'en_US', skip_welcome_mail = False,
                 uid_extern: str = None) -> dict:
        """
        Function to add a mail
        :param mail: the mail to add
        :param password: the password for the mail
        :param plan: the plan of the mail
        :param first_name: the first name of the mail
        :param last_name: the last name of the mail
        :param inboxsave: True if the mail should be saved into the inbox folder (relevant for forwards)
        :param forwards: List of addresses to forwards mails to
        :param memo: Memo of the mail
        :param language: the language of the mail in locale format
        :param skip_welcome_mail: True if the welcome mail should be skipped, False if it should be sent
        :param uid_extern: the external UID of the mail
        :return: the response for the request
        """
        if forwards is None:
            forwards = []
        if memo is None:
            memo = ''
        return self.api_request('mail.add',{'mail':mail, 'password':password, 'plan':plan,
                                                    'first_name':first_name, 'last_name':last_name,
                                                    'inboxsave':inboxsave, 'forwards':forwards, 'memo':memo,
                                                    'language':language, 'skip_welcome_mail':skip_welcome_mail,
                                                    'uid_extern':uid_extern})

    def mail_get(self, mail: str, include_quota_usage: bool = False) -> dict:
        """
        Function to retrieve a mail address
        :param mail: the mail to retrieve
        :param include_quota_usage: True if the quota usage should be included in the request
        :return the response for the request
        """
        return self.api_request('mail.get', {'mail':mail, 'include_quota_usage':include_quota_usage})

    def mail_get_object(self, mail:str) -> Mail:
        result = self.api_request('mail.get', {'mail':mail, 'include_quota_usage':False})
        mail_object = Mail(mail)
        for k, v in result.items():
            if v:
                setattr(mail_object, k, v)
        return mail_object

    def mail_set(self, mail: str, **kwargs):
        """
        Function to update a mail
        :param mail: the mail to update
        :param kwargs: Optional arguments corresponding to API parameters (e.g., password, plan)
                       See API documentation for full list.
        :return:
        """
        if 'password' in kwargs and 'password_hash' in kwargs:
          raise KeyError('''Simultaneous usage of 'password' and 'password_hash' not allowed.''')
        
        # Check for each argument in kwargs if it is a valid function parameter.
        # Check key and type of value. Raise errors if a check fails.
        for arg in kwargs:
          if arg not in mail_set_attributes:
            raise ValueError('Parameter', arg, 'not a valid parameter for mail_set')
          
          if type(kwargs[arg]) != mail_set_attributes[arg]:
            raise TypeError('Attribute', arg, 'must be of type',
              str(mail_set_attributes[arg]) + '.', str(type(kwargs[arg])), 'given.')
            
        # After validation, build parameter list from mail and kwargs
        params = {'mail':mail}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        
        return self.api_request('mail.set', params)

    def mail_set_password(self, mail: str, password: str) -> dict:
        """
        Function to set a new password for a mail
        :param mail: the mail to set the password for
        :param password: the password to set
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail':mail, 'password':password})

    def mail_set_password_require_reset(self, mail: str, password: str) -> dict:
        """
        Function to set a new password for a mail and force the user to set a new password on the next login
        :param mail: the mail to set the password for
        :param password: the password to set
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail': mail, 'password': password, 'require_reset': True})

    def mail_set_plan(self, mail: str, plan: str) -> dict:
        """
        Function to set a new plan for a mail
        :param mail: the mail to set the plan for
        :param plan: the plan to set
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail':mail, 'plan':plan})

    def mail_set_forwards(self, mail: str, forwards: list) -> dict:
        """
        Function to set mail forwards
        :param mail: the mail to set the forwards for
        :param forwards: a list of addresses to forwards mails to
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail':mail, 'forwards':forwards})

    def mail_set_aliases(self, mail: str, aliases: list) -> dict:
        """
        Function to set mail aliases
        :param mail: the mail to set the aliases for
        :param aliases: a list of aliases to set
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail':mail, 'aliases':aliases})

    def mail_set_state(self, mail: str, active: bool) -> dict:
        """
        Function to activate or deactivate a mail
        :param mail: the mail to set the status for
        :param active: True if the mail should be active, False if it shall be deactivated
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail':mail, 'active':active})

    def mail_set_deletion_date(self, mail: str, deletion_date: str) -> dict:
        """
        Function to delete an inbox at a given date.
        To unset, use mail_set_state and set 'active = True'
        :param mail: the mail to delete
        :param deletion_date: the date to delete the mail on
        :return: the response for the request
        """
        return self.api_request('mail.set', {'mail': mail, 'deletion_date': deletion_date,
                                'active': False})

    def mail_capabilities_set(self, mail: str, capabilties: dict) -> dict:
        """
        Function to set a domain capabilities
        :param mail: the mail to set the capabilities for
        :param capabilties: a list of capabilities to set for the domain
        :return: the API response
        """
        params = {'mail': mail}
        for attribute in capabilties:
            if attribute not in mail_capabilities:
                raise ValueError(attribute, 'not found')
            params.update({attribute: capabilties[attribute]})
        return self.api_request('mail.capabilities.set', params)

    def mail_del(self, mail: str) -> dict:
        """
        Function to delete a mail
        :param mail: the mail to delete
        :return: the response for the request
        """
        return self.api_request('mail.del', {'mail':mail})

    def mail_apppassword_list(self, mail:str) -> dict:
        """
        Function to list all app passwords of a given mail
        :param mail: the mail to list app passwords for
        :return: the response for the request
        """
        return self.api_request('mail.apppassword.list', {'mail':mail})

    def mail_apppassword_add(self, mail:str, memo:str, imap_allowed:bool = True, smtp_allowed:bool = True) -> dict:
        """
        Function to generate a new mail app password for a mail
        :param mail: the mail to generate a new mail app password
        :param memo: memo of the app password
        :param imap_allowed: True if the app password should be allowed to use an IMAP server. Default: True
        :param smtp_allowed: True if the app password should be allowed to use an SMTP server. Default: True
        :return: the response for the request
        """
        return self.api_request('mail.apppassword.add', {'mail':mail, 'memo':memo,
                                                         'imap_allowed':imap_allowed, 'smtp_allowed':smtp_allowed})

    def mail_apppassword_del(self, apppassword_id: int) -> dict:
        """
        Function to delete a mail app password
        :param apppassword_id: the id of the mail app password
        :return: the response for the request
        """
        return self.api_request('mail.apppassword.del', {'id':apppassword_id})

    def mail_externaluid(self, account: str, uid_extern: str) -> dict:
        """
        Function to get a mail using an external UID
        :param account: the account to get a mail for
        :param uid_extern: the external UID to get a mail for
        :return: mailbox API response - an array with the mail details
        """
        return self.api_request('mail.externaluid', {'account':account, 'uid_extern':uid_extern})

    def mail_backup_list(self, mail: str) -> dict:
        """
        Function to list all backups for a given mail
        :param mail: the mail to list backups for
        :return: mailbox API response - an array with the backup numbers and dates
        """
        return self.api_request('mail.backup.list', {'mail':mail})

    def mail_backup_import(self, mail: str, backup_id: str, time: str, backup_filter: str) -> dict:
        """
        Function to import a backup for a mail
        :param mail: the mail to import
        :param backup_id: the id of the backup
        :param time: the time of the backup
        :param backup_filter: the filter of the backup - "all" or an IMAP foldername
        :return: mailbox API response - an array with the backup numbers and dates
        """
        return self.api_request('mail.backup.import',
                                {'mail':mail, 'id':backup_id, 'time':time, 'filter':backup_filter})

    def mail_spamprotect_get(self, mail: str) -> dict:
        """
        Function to retrieve the spam settings for a given mail
        :param mail: the mail to get the spam settings for
        :return: mailbox API response - an array with the spam settings
        """
        return self.api_request('mail.spamprotect.get', {'mail':mail})

    def mail_spamprotect_set(self, mail: str, greylist: bool, smtp_plausibility: bool, rbl: bool,
                             bypass_banned_checks: bool, tag2level: float, killlevel: str, route_to: str) -> dict:
        """
        Function to set the spam settings for a given mail
        :param mail: the mail to set the spam settings for
        :param greylist: (de-)activation of greylisting for the mail
        :param smtp_plausibility: (de-)activation of SMTP plausibility checks for the mail
        :param rbl: (de-)activation of Real-time Blacklist checks for the mail
        :param bypass_banned_checks: (de-)activation of checks for executable files
        :param tag2level: float value for the spam filter (e.g. 5.5). Will be rounded to 1 decimal place
        :param killlevel: reject or redirection of spam mails. Allowed values: 'reject' or 'redirection'
        :param route_to: folder to route spam to
        :return: mailbox API response - an array with the spam settings
        """

        if killlevel not in ('reject', 'route'):
            raise ValueError('''Invalid value for killlevel. Only 'reject' or 'route' are allowed''')

        return self.api_request('mail.spamprotect.set',
                                {'mail':mail, 'greylist': bool2str(greylist),
                                 'smtp_plausibility':bool2str(smtp_plausibility), 'rbl':bool2str(rbl),
                                 'bypass_banned_checks':bool2str(bypass_banned_checks), 'tag2level':round(tag2level, 1),
                                 'killevel':killlevel, 'route_to':route_to})

    def mail_blacklist_list(self, mail: str) -> dict:
        """
        Function to list the mail blacklist for a given mail address
        :param mail: the mail to list the blacklist for
        :return: mailbox API response - an array with the complete blacklist of the mail
        """
        return self.api_request('mail.blacklist.list', {'mail':mail})

    def mail_blacklist_add(self, mail: str, add_address: str) -> dict:
        """
        Function to add a mail to a blacklist of a mail address
        :param mail: the mail of the owner of the blacklist
        :param add_address: the address to add to the blacklist
        :return: mailbox API response - an array with the complete blacklist of the mail
        """
        return self.api_request('mail.blacklist.add', {'mail':mail, 'add_address':add_address})

    def mail_blacklist_delete(self, mail: str, delete_address: str) -> dict:
        """
        Function to delete a mail from a blacklist
        :param mail: the mail of the owner of the blacklist
        :param delete_address: the address to delete from the blacklist
        :return: mailbox API response - an array with the complete blacklist of the mail
        """
        return self.api_request('mail.blacklist.remove', {'mail':mail, 'delete_address':delete_address})

    def mail_vacation_get(self, mail: str) -> dict:
        """
        Function to get the vacation notice for a given mail
        :param mail: the mail to get the vacation notice for
        :return: mailbox API response - the vacation notice of the mail
        """
        return self.api_request('mail.vacation.get', {'mail':mail})

    def mail_vacation_set(self, mail: str, subject: str, body: str, start_date: str, end_date: str,
                          additional_mail_addresses: list = None) -> dict:
        """
        Function to set the vacation notice for a given mail
        :param mail: the mail to get the vacation notice for
        :param subject: the subject of the vacation notice
        :param body: the body of the vacation notice (optional)
        :param start_date: the start date of the vacation notice in format YYYY-MM-DD
        :param end_date: the end date of the vacation notice in format YYYY-MM-DD
        :param additional_mail_addresses: list of addresses to add to the vacation notice (optional)
        :return: mailbox API response - array with result 'true' of the request, code and message in case of an error
        """
        params = {'mail':mail, 'subject':subject, 'body':body,'start_date':start_date, 'end_date':end_date,
                  'additional_mail_addresses':additional_mail_addresses}

        # If no additional_mail_addresses are given, remove the parameter from the request
        if not additional_mail_addresses:
            params.pop('additional_mail_addresses')

        return self.api_request('mail.vacation.set', params)

    def group_list(self) -> dict:
        """
        Function to list all groups for an account
        :return: mailbox API response - the list of groups
        """
        return self.api_request('group.list', {})

    def group_get(self, group_id: int) -> dict:
        """
        Function to get a group from the account by the group id
        :param group_id: the id of the group to get
        :return: mailbox API response - the list of groups of the account
        """
        return self.api_request('group.get', {'group_id':group_id})

    def group_del(self, group_id: int) -> dict:
        """
        Function to delete a group
        :param group_id: the group's id of the group to delete
        :return: mailbox API response - True if the group was deleted, False otherwise
        """
        return self.api_request('group.del', {'group_id':group_id})

    def group_add(self, name: str, display_name: str, mail_addresses_to_add: list) -> dict:
        """
        Function to add a group
        :param name: the group name
        :param display_name: the group's display name
        :param mail_addresses_to_add: a list of mail addresses to add
        :return: mailbox API response - True if the group was added, False otherwise
        """
        return self.api_request('group.add', {'name':name, 'display_name':display_name,
                                              'mail_addresses_to_add':mail_addresses_to_add})

    def group_set(self, group_id: int, display_name: str, mail_addresses_to_add: list = None,
                  mail_addresses_to_remove: list = None) -> dict:
        """
        Function to modify a group. Either mail_addresses_to_add or mail_addresses_to_remove have to be specified.
        :param group_id: the group's id of the group to modify
        :param display_name: the group's display name
        :param mail_addresses_to_add: a list of mail addresses to add. Defaults to None
        :param mail_addresses_to_remove: a list of mail addresses to remove. Defaults to None
        :return: mailbox API response - True if the group was edited, False otherwise
        """
        # If mail_addresses_to_add and mail_addresses_to_remove are both empty, raise error
        if mail_addresses_to_add is None and mail_addresses_to_remove is None:
            raise ValueError('mail_addresses_to_add or mail_addresses_to_remove are required')

        return self.api_request('group.set', {'group_id':group_id, 'display_name':display_name,
                                              'mail_addresses_to_add':mail_addresses_to_add,
                                              'mail_addresses_to_remove':mail_addresses_to_remove})

    def mail_passwordreset_listmethods(self, mail: str) -> dict:
        """
        Function to list all available password reset methods for a given mail
        :param mail: the mail to query
        :return: mailbox API response - a list of available password reset methods
        """
        return self.api_request('mail.passwordreset.listmethods', {'mail':mail})

    def mail_passwordreset_sendsms(self, mail: str, cell_phone: str) -> dict:
        """
        Function to send a password reset for a mail via SMS
        :param mail: the mail to send the SMS for
        :param cell_phone: the cell phone number of the mailbox
        :return: mailbox API response - True if the SMS was sent, False otherwise
        """
        return self.api_request('mail.passwordreset.sendsms',{'mail':mail, 'cell_phone':cell_phone})

    def mail_passwordreset_setpassword(self, mail: str, token: str, password: str) -> dict:
        """
        Function to set a password reset for a mail using a token
        :param mail: the mail to set the password for
        :param token: the token to set the password
        :param password: the new password to set
        :return: mailbox API response - True if the password was set, False otherwise
        """
        return self.api_request('mail.passwordreset.setpassword',
                                {'mail':mail, 'token':token, 'password':password})

    def context_list(self, account: str) -> dict:
        """
        Function to list all contexts of a given account
        :param account: the account to list all contexts for
        :return: mailbox API response - an array with key 'context id' and value 'associated domains'
        """
        return self.api_request('context.list', {'account':account})

    def search(self, search_string: str) -> dict:
        """
        Function to search for accounts, domains and email addresses
        :param search_string: the query to search by
        :return: the mailbox API response for the request - an array with results for accounts, domains and mailboxes
        """
        return self.api_request('search', {'search':search_string})

    def mailinglist_list(self, account: str) -> dict:
        """
        Function to list all mailing lists for a given account
        :param account: the account to list all mailing lists for
        :return: a dict containing the list of mailing lists
        """
        return self.api_request('mailinglist.list', {'account':account})

    def mailinglist_add(self, mailinglist: str, password: str, account: str, adminmail: str = None) -> dict:
        """
        Function to add a mailing list
        :param mailinglist: the mailing list to add
        :param password: the password of the mailing list
        :param account: the account of the mailing list
        :param adminmail: admin email address of the mailing list (optional)
        :return: True if the mailing list was added, error code otherwise
        """
        return self.api_request('mailinglist.add', {'mailinglist':mailinglist, 'password':password,
                                                'account':account, 'adminmail':adminmail})

    def mailinglist_get(self, mailinglist: str, account: str) -> dict:
        """
        Function to get a mailing list
        :param mailinglist: the mailing list to get
        :param account: the account of the mailing list
        :return: the mailbox API response for the request - a dict of the mailing list
        """
        return self.api_request('mailinglist.get', {'mailinglist':mailinglist, 'account':account})

    def mailinglist_set(self, mailinglist: str, account: str, password: str = None, adminmail: str = None) -> dict:
        """
        Function to change a mailing list
        :param mailinglist: the mailing list to change
        :param password: the password of the mailing list
        :param account: the account of the mailing list (optional)
        :param adminmail: admin email address of the mailing list (optional)
        :return: the mailbox API response for the request - True if the mailing list was changed, error code otherwise
        """
        return self.api_request('mailinglist.set', {'mailinglist':mailinglist, 'account':account,
                                                'password':password, 'adminmail':adminmail})

    def mailinglist_delete(self, mailinglist: str, account: str) -> dict:
        """
        Function to delete a mailing list
        :param mailinglist: the mailing list to delete
        :param account: the account of the mailing list
        :return: the mailbox API response for the request - True if the mailing list was deleted, error code otherwise
        """
        return self.api_request('mailinglist.delete', {'mailinglist':mailinglist, 'account':account})

    def additionalmailaccount_add(self, parent_mail: str, new_account_mail: str, new_account_password: str,
                                  primary_address: str = None, mail_server: str = 'imap.mailbox.org',
                                  mail_port: int = 993, mail_secure: bool = True, mail_starttls: bool = False,
                                  transport_server: str = 'smtp.mailbox.org', transport_port: int = 465,
                                  transport_secure: bool = True, transport_starttls: bool = False,
                                  trash_folder: str = 'Trash', sent_folder: str = 'Sent', drafts_folder: str = 'Drafts',
                                  spam_folder: str = 'Junk') -> dict:
        """
        Function to add an extra mail account to a mail address. Default values are the values of mailbox.org.
        Order and syntax of the call deviate slightly from the mailbox.org API:
        1. parent_mail is the first argument
        2. mail server settings are grouped
        3. transport server settings are grouped
        4. Ports are integers
        :param new_account_mail: the additional mail address to add
        :param new_account_password: the password of the additional mail address
        :param parent_mail: the mail address to add the additional mail account to
        :param primary_address: the primary 'address from' for the additional mail address
        :param mail_server: the IMAP server to use
        :param mail_port: the port of the IMAP server
        :param transport_server: the SMTP server to use
        :param transport_port: the port of the SMTP server
        :param mail_secure: whether to use SSL for IMAP
        :param mail_starttls: whether to use STARTTLS for IMAP
        :param transport_secure: whether to use SSL for SMTP
        :param transport_starttls: whether to use STARTTLS for SMTP
        :param trash_folder: name of the trash folder
        :param sent_folder: name of the sent folder
        :param drafts_folder: name of the drafts folder
        :param spam_folder: name of the spam folder
        :return: the response for the request - True if adding was successful, error code otherwise
        """
        return self.api_request('additionalmailaccount.add', {'new_account_mail': new_account_mail,
                                                              'new_account_password': new_account_password,
                                                              'parent_mail': parent_mail,
                                                              'primary_address': primary_address,
                                                              'mail_server': mail_server, 'mail_port': str(mail_port),
                                                              'transport_server': transport_server,
                                                              'transport_port': str(transport_port),
                                                              'mail_secure': mail_secure,
                                                              'mail_starttls': mail_starttls,
                                                              'transport_secure': transport_secure,
                                                              'transport_starttls': transport_starttls,
                                                              'trash_folder': trash_folder,
                                                              'sent_folder': sent_folder,
                                                              'drafts_folder': drafts_folder,
                                                              'spam_folder': spam_folder})

    def additionalmailaccount_delete(self, parent_mail: str, account_mail: str) -> dict:
        """
        Function to delete an additional mail account
        :param parent_mail: the mail address to delete
        :param account_mail: the account to delete
        :return: True if the account was deleted, error code otherwise
        """
        return self.api_request('additionalmailaccount.delete',
                                {'parent_mail':parent_mail, 'account_mail':account_mail})

def bool2str(state: bool) -> str:
    """
    Converts a boolean value to '1' if True, and '0' if False...
    ...because that's how the mailbox.org API expects things.
    """
    if state:
        return '1'
    return '0'