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

class APIClient:
    """
    Object for API Client
    """

    def __init__(self):
        # URL of the API
        self.url = "https://api.mailbox.org/v1/"

        # JSON RPC ID - a unique ID is required for each request during a session
        self.jsonrpc_id = 0
        self.level = None
        self.auth_id = None

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
        print('API request:\t', request)

        api_response = requests.post(
            self.url, data=json.dumps(request), headers=headers).json()
        print('API full response:\t', api_response)

        # Depending on the type of response the return changes.
        # If a successful result, only the result is returned
        if 'result' in api_response:
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
        api_response = self.api_request('hello.world',{})
        return api_response

    def hello_innerworld(self):
        """
        Hello World function to test the authentication
        :return: The response from the mailbox.org Business API
        """
        api_response = self.api_request('hello.innerworld', {})
        return api_response

    def domain_list(self, account: str) -> dict:
        """
        Function to list all domains
        :param account: the account to list domains for
        :return: the API response
        """
        api_response = self.api_request('domain.list',{'account':account})
        return api_response

    def domain_add(self, account: str, domain: str, password: str) -> dict:
        """
        Function to add a domain
        :param account: the account to add a domain for
        :param domain: the domain to add
        :param password: the password of the domain
        :return: the API response
        """
        api_response = self.api_request('domain.add', {'account':account, 'domain':domain, 'password':password})
        return api_response

    def domain_get(self, domain: str) -> dict:
        """
        Function to get a specific domain
        :param domain: the domain to get
        :return: the API response
        """
        api_response = self.api_request('domain.get',{'domain':domain})
        return api_response

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
        api_response = self.api_request('domain.capabilities.set', params)
        return api_response

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

        api_response = self.api_request('domain.set', params)
        return api_response

    def domain_del(self, account: str, domain: str) -> dict:
        """
        Function to delete a domain
        :param account: the account to delete a domain in
        :param domain: the domain to delete
        :return: the API response
        """
        api_response = self.api_request('domain.del', {'account':account, 'domain':domain})
        return api_response

    def mail_list(self, domain) -> dict:
        """
        Function to list all mailboxes
        :return: the response from the mailbox.org Business API
        """
        api_response = self.api_request('mail.list', {'domain':domain})
        return api_response

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
        api_response = self.api_request('mail.add',{'mail':mail, 'password':password, 'plan':plan,
                                                    'first_name':first_name, 'last_name':last_name,
                                                    'inboxsave':inboxsave, 'forwards':forwards, 'memo':memo,
                                                    'language':language, 'uid_extern':uid_extern})
        return api_response

    def mail_get(self, mail: str):
        """
        Function to retrieve a mail address
        :param mail: the mail to retrieve
        :return the response for the request
        """
        api_response = self.api_request('mail.get', {'mail':mail})
        return api_response

    def mail_set(self, mail:str, attributes: dict):
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
        api_response = self.api_request('mail.set', params)
        return api_response

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
        api_response = self.api_request('mail.capabilities.set', params)
        return api_response

    def mail_del(self, mail: str) -> dict:
        """
        Function to delete a mail
        :param mail: the mail to delete
        :return: the response for the request
        """
        api_response = self.api_request('mail.del', {'mail':mail})
        return api_response

    def mail_apppassword_list(self, mail:str) -> dict:
        """
        Function to list all app passwords of a given mail
        :param mail: the mail to list app passwords for
        :return: the response for the request
        """
        api_response = self.api_request('mail.apppassword.list', {'mail':mail})
        return api_response

    def mail_apppassword_add(self, mail:str, memo:str) -> dict:
        """
        Function to generate a new mail app password for a mail
        :param mail: the mail to generate a new mail app password
        :param memo: memo of the app password
        :return: the response for the request
        """
        api_response = self.api_request('mail.apppassword.add', {'mail':mail, 'memo':memo})
        return api_response

    def mail_apppassword_delete(self, apppassword_id: int) -> dict:
        """
        Function to delete a mail app password
        :param apppassword_id: the id of the mail app password
        :return: the response for the request
        """
        api_response = self.api_request('mail.apppassword.delete', {'id':apppassword_id})
        return api_response

    def context_list(self, account: str) -> dict:
        """
        Function to list all contexts of a given account
        :param account: the account to list all contexts for
        :return: the response for the request
        """
        api_response = self.api_request('context.list', {'account':account})
        return api_response


