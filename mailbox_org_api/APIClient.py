"""
Module for the BMBO API client
"""
import json
import requests

headers = {'content-type': 'application/json'}
domain_capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST', 'MAIL_BACKUPRECOVER', 'MAIL_PASSWORDRESET_SMS']
mail_capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST', 'MAIL_BACKUPRECOVER', 'MAIL_OTP', 'MAIL_PASSWORDRESET_SMS']
mail_set_arguments = {'password': str, 'password_hash': str, 'same_password_allowed': bool,
                      'require_password_reset': bool, 'plan': str, 'additional_mail_quota': str,
                      'additional_cloud_quota': str, 'first_name': str, 'last_name': str, 'inboxsave': bool,
                      'forwards': list, 'aliases': list, 'alternate_mail': str, 'memo': str, 'allow_nets': str,
                      'active': bool, 'title': str, 'birthday': str, 'position': str, 'department': str, 'company': str,
                      'street': str, 'postal_code': str, 'city': str, 'phone': str, 'fax': str, 'cell_phone': str,
                      'uid_extern': str, 'language': str}
account_set_arguments = {'password': str, 'plan': str, 'memo': str, 'address_main_first_name': str,
                         'address_main_last_name':str, 'address_main_street	': str, 'address_main_zipcode': str,
                         'address_main_town': str, 'address_main_country': str,	'address_payment_first_name': str,
                         'address_payment_last_name': str, 'address_payment_street': str,
                         'address_payment_zipcode': str, 'address_payment_town': str, 'company': str, 'bank_iban': str,
                         'bank_bic': str, 'bank_account_owner': str, 'av_contract_accept_name': str,
                         'contact_mail': str, 'contact_mail_payment': str, 'contact_phone': str, 'contact_fax': str,
                         'tarifflimits': list, 'av_contract_professional_secrecy': bool}

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
            print('API request:\t', request)

        api_response = requests.post(
            self.url, data=json.dumps(request), headers=headers).json()
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
            print(api_response['error'])
            return api_response['error']

        # If neither a success nor an error, the full response if returned
        else:
            return api_response

    def auth(self, username, password) -> dict:
        """
        Function to authenticate and create a new API session
        :param username: the username
        :param password: the password
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

    def account_add(self, account: str) -> dict:
        """
        Function to create a new account
        :param account: the account name to create
        :return: the response from the mailbox.org Business API
        """
        return self.api_request('account.add', {'account':account})

    def account_get(self, account: str) -> dict:
        """
        Function to get a specific account
        :param account: the account name to get
        :return: the response from the mailbox.org Business API
        """
        return self.api_request('account.get', {'account':account})

    def account_set(self, account: str, attributes: dict) -> dict:
        """
        Function to update a specific account
        :param account: the account name to update
        :param attributes: the attributes to update
        :return: the response from the mailbox.org Business API
        """
        params = {'account':account}
        for attribute in attributes:
            print('Attribute:', attribute)
            if attribute not in account_set_arguments:
                raise ValueError(attribute, 'not found')
            if type(attributes[attribute]) != account_set_arguments[attribute]:
                errormsg = ('Attribute ' + attribute + ' must be of type ' + str(account_set_arguments[attribute]) + '. '
                            + str(type(attributes[attribute])) + ' provided.')
                raise TypeError(errormsg)
            params.update({attribute: attributes[attribute]})
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
        Function to get a specific of all invoices for an account
        :param account: the account name
        :param token: the token for the invoice
        :return: the response from the mailbox.org Business API - the invoice as a Base64 encoded gzipped string
        """
        return self.api_request('account.invoice.get', {'account':account, 'token':token})

    def account_invoice_get_list(self, account: str) -> list:
        """
        Function to get a list of all invoice id's for a specific account
        """
        response = self.api_request('account.invoice.list', {'account':account})
        invoices = []

        for invoice in response:
            invoices.append(invoice['invoice_id'])

        return invoices

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

    def account_invoice_get_pdf(self, account: str, invoice_id: str) -> bytes:
        """
        Function to get a specific invoice as a PDf-file
        :param account: the account name
        :param invoice_id: the invoice ID
        :return: the PDF as bytes
        """
        import base64
        import zlib

        # Get the token and retrieve the invoice data
        response = self.api_request('account.invoice.get',
                                    {'account': account,
                                     'token': self.account_invoice_get_token(account, invoice_id)})

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

    def domain_capabilities_set(self, domain: str, capabilties: dict) -> dict:
        """
        Function to set a domain capabilities
        :param domain: the domain to set the capabilities for
        :param capabilties: a list of capabilities to set for the domain
        :return: the API response
        """
        params = {'domain': domain}
        for element in capabilties:
            if element not in domain_capabilities:
                break
            params.update({element: capabilties[element]})
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

    def mail_list(self, domain) -> dict:
        """
        Function to list all mailboxes
        :return: the response from the mailbox.org Business API
        """
        return self.api_request('mail.list', {'domain':domain})

    def mail_add(self, mail:str, password: str, plan: str, first_name: str, last_name: str, inboxsave: bool = True,
                 forwards: list = None, memo: str = None, language: str = 'en_EN', uid_extern: str = None) -> dict:
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
                                                    'language':language, 'uid_extern':uid_extern})

    def mail_get(self, mail: str, include_quota_usage: bool = False) -> dict:
        """
        Function to retrieve a mail address
        :param mail: the mail to retrieve
        :param include_quota_usage: True if the quota usage should be included in the request
        :return the response for the request
        """
        return self.api_request('mail.get', {'mail':mail, 'include_quota_usage':include_quota_usage})

    def mail_set(self, mail: str, attributes: dict):
        """
        Function to update a mail
        :param mail: the mail to update
        :param attributes: dict of the attributes to update
        :return:
        """
        params = {'mail':mail}
        for attribute in attributes:
            print('Attribute:', attribute)
            if attribute not in mail_set_arguments:
                raise ValueError(attribute, 'not found')
            if type(attributes[attribute]) != mail_set_arguments[attribute]:
                errormsg = ('Attribute ' + attribute + ' must be of type ' + str(mail_set_arguments[attribute]) + '. '
                            + str(type(attributes[attribute])) + ' provided.')
                raise TypeError(errormsg)
            params.update({attribute: attributes[attribute]})
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

    def mail_apppassword_add(self, mail:str, memo:str) -> dict:
        """
        Function to generate a new mail app password for a mail
        :param mail: the mail to generate a new mail app password
        :param memo: memo of the app password
        :return: the response for the request
        """
        return self.api_request('mail.apppassword.add', {'mail':mail, 'memo':memo})

    def mail_apppassword_delete(self, apppassword_id: int) -> dict:
        """
        Function to delete a mail app password
        :param apppassword_id: the id of the mail app password
        :return: the response for the request
        """
        return self.api_request('mail.apppassword.delete', {'id':apppassword_id})

    def mail_externaluid(self, mail: str) -> dict:
        """
        Function to get a mail using an external UID
        :param mail: the mail to get
        :return: the response for the request
        """
        return self.api_request('mail.externaluid', {'mail':mail})

    def mail_backup_list(self, mail: str) -> dict:
        """
        Function to list all backups for a given mail
        :param mail: the mail to list backups for
        :return: the response for the request - a list of backups
        """
        return self.api_request('mail.backup.list', {'mail':mail})

    def mail_backup_import(self, mail: str, id: str, time: str, filter: str) -> dict:
        """
        Function to import a backup for a mail
        :param mail: the mail to import
        :param id: the id of the backup
        :param time: the time of the backup
        :param filter: the filter of the backup - "all" or an IMAP foldername
        """
        return self.api_request('mail.backup.import',
                                {'mail':mail, 'id':id, 'time':time, 'filter':filter})

    def mail_spamprotect_get(self, mail: str) -> dict:
        """
        Function to retrieve the spam settings for a given mail
        :param mail: the mail to get the spam settings for
        :return: the response for the request - the spam settings
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
        """

        if killlevel not in ('reject', 'route'):
            raise ValueError('''Invalid value for killlevel. Only 'reject' or 'route' are allowed''')

        return self.api_request('mail.spamprotect.set',
                                {'greylist': bool2str(greylist),
                                 'smtp_plausibility':bool2str(smtp_plausibility), 'rbl':bool2str(rbl),
                                 'bypass_banned_checks':bool2str(bypass_banned_checks), 'tag2level':round(tag2level, 1),
                                 'killlevel':killlevel, 'route_to':route_to})

    def mail_blacklist_list(self, mail: str) -> dict:
        """
        Function to list the mail blacklist for a given mail address
        :param mail: the mail to list the blacklist for
        :return: the response for the request - the blacklist of the mail
        """
        return self.api_request('mail.blacklist.list', {'mail':mail})

    def mail_blacklist_add(self, mail: str, add_address: str) -> dict:
        """
        Function to add a mail to a blacklist of a mail address
        :param mail: the mail of the owner of the blacklist
        :param add_address: the address to add to the blacklist
        """
        return self.api_request('mail.blacklist.add', {'mail':mail, 'add_address':add_address})

    def mail_blacklist_delete(self, mail: str, delete_address: str) -> dict:
        """
        Function to delete a mail from a blacklist
        :param mail: the mail of the owner of the blacklist
        :param delete_address: the address to delete from the blacklist
        """
        return self.api_request('mail.blacklist.remove', {'mail':mail, 'delete_address':delete_address})

    def mail_vacation_get(self, mail: str) -> dict:
        """
        Function to get the vacation notice for a given mail
        :param mail: the mail to get the vacation notice for
        :return: the vacation notice of the mail. Message, subject, body, additional addresses, start date, end date
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
        """
        return self.api_request('mail.vacation.set', {'mail':mail, 'subject':subject, 'body':body,
                                                      'start_date':start_date, 'end_date':end_date,
                                                      'additional_mail_addresses':additional_mail_addresses})

    def group_list(self) -> dict:
        """
        Function to list all groups for an account
        """
        return self.api_request('group.list', {})

    def group_add(self, name: str, display_name: str, mail_addresses_to_add: list) -> dict:
        """
        Function to add a group
        :param name: the group name
        :param display_name: the group's display name
        :param mail_addresses_to_add: a list of mail addresses to add
        """
        return self.api_request('group.add', {'name':name, 'display_name':display_name,
                                              'mail_addresses_to_add':mail_addresses_to_add})

    def group_set(self, name: str, display_name: str, mail_addresses_to_add: list, mail_addresses_to_remove: list) -> dict:
        """
        Function to modify a group
        :param name: the group name
        :param display_name: the group's display name
        :param mail_addresses_to_add: a list of mail addresses to add
        :param mail_addresses_to_remove: a list of mail addresses to remove
        """
        return self.api_request('group.set', {'name':name, 'display_name':display_name,
                                              'mail_addresses_to_add':mail_addresses_to_add,
                                              'mail_addresses_to_remove':mail_addresses_to_remove})

    def mail_passwordreset_listmethods(self, mail: str) -> dict:
        """
        Function to list all available password reset methods for a given mail
        :param mail: the mail to query
        :return: the response for the request - a list of available password reset methods
        """
        return self.api_request('mail.passwordreset.listmethods', {'mail':mail})

    def mail_passwordreset_sendsms(self, mail: str, cell_phone: str) -> dict:
        """
        Function to send a password reset for a mail via SMS
        :param mail: the mail to send the SMS for
        :param cell_phone: the cell phone number of the mailbox
        :return: the response for the request
        """
        return self.api_request('mail.passwordreset.sendsms',{'mail':mail, 'cell_phone':cell_phone})

    def mail_passwordreset_setpassword(self, mail: str, token: str, password: str) -> dict:
        """
        Function to set a password reset for a mail using a token
        :param mail: the mail to set the password for
        :param token: the token to set the password
        :param password: the new password to set
        """
        return self.api_request('mail.passwordreset.setpassword',
                                {'mail':mail, 'token':token, 'password':password})

    def group_del(self, name: str) -> dict:
        """
        Function to delete a group
        :param name: the group's name
        """
        return self.api_request('group.delete', {'name':name})

    def context_list(self, account: str) -> dict:
        """
        Function to list all contexts of a given account
        :param account: the account to list all contexts for
        :return: the response for the request
        """
        return self.api_request('context.list', {'account':account})

    def search(self, search_string: str) -> dict:
        """
        Function to search for accounts, domains and email addresses
        :param search_string: the query to search by
        :return: the response for the request
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
        :return: dict of the mailing list
        """
        return self.api_request('mailinglist.get', {'mailinglist':mailinglist, 'account':account})

    def mailinglist_set(self, mailinglist: str, account: str, password: str = None, adminmail: str = None) -> dict:
        """
        Function to change a mailing list
        :param mailinglist: the mailing list to change
        :param password: the password of the mailing list
        :param account: the account of the mailing list (optional)
        :param adminmail: admin email address of the mailing list (optional)
        :return: True if the mailing list was changed, error code otherwise
        """
        return self.api_request('mailinglist.set', {'mailinglist':mailinglist, 'account':account,
                                                'password':password, 'adminmail':adminmail})

    def mailinglist_delete(self, mailinglist: str, account: str) -> dict:
        """
        Function to delete a mailing list
        :param mailinglist: the mailing list to delete
        :param account: the account of the mailing list
        :return: True if the mailing list was deleted, error code otherwise
        """
        return self.api_request('mailinglist.delete', {'mailinglist':mailinglist, 'account':account})

    def additionalmailaccount_add(self, parent_mail: str, new_account_mail: str, new_account_password: str,
                                  primary_address: str, mail_server: str = 'imap.mailbox.org', mail_port: int = 993,
                                  mail_secure: bool = True, mail_starttls: bool = False,
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