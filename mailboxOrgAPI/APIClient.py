"""
Module for the BMBO API client
"""
import json
import requests

headers = {'content-type': 'application/json'}

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
        # print('Headers:', headers)
        print('API request:\t', request)

        api_response = requests.post(
            self.url, data=json.dumps(request), headers=headers).json()
        print('API response:\t', api_response)
        return api_response['result']

    def auth(self, username, password) -> dict:
        api_response = self.api_request('auth', {'user':username, 'pass':password})
        if api_response['session']:
            self.level = api_response["level"]
            self.auth_id = str(api_response["session"])
            headers.update({"HPLS-AUTH": self.auth_id})

        print('Level:', self.level)
        print('Auth ID:', self.auth_id)
        return api_response


    def deauth(self) -> bool:
        """
        Function to close the current API session
        :return: True if the API session is closed, False otherwise
        """
        api_response = self.api_request('deauth',{})
        if api_response:
            del headers["HPLS-AUTH"]
            return True
        return False

    def hello_world(self):
        api_response = self.api_request('hello.world',{})
        return api_response

    def hello_innerworld(self):
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


    def mail_list(self, domain) -> dict:
        """
        Function to list all mailboxes
        :return: the response from the mailbox.org Business API
        """
        api_response = self.api_request('mail.list', {'domain':domain})
        return api_response

    def mail_add(self, mail:str, password: str, plan: str, first_name: str, last_name: str, inboxsave: bool = True,
                 forwards=None):
        """
        Function to add a mail
        :param mail: the mail to add
        :param password: the password for the mail
        :param plan: the plan of the mail
        :param first_name: the first name of the mail
        :param last_name: the last name of the mail
        :param inboxsave: True if the mail should be saved into the inbox folder (relevant for forwards)
        :param forwards: List of addresses to forwards mails to
        :return: the response for the request
        """
        if forwards is None:
            forwards = []
        api_response = self.api_request('mail_.dd',{'mail':mail, 'password':password, 'plan':plan,
                                                    'first_name':first_name, 'last_name':last_name,
                                                    'inboxsave':inboxsave, 'forwards':forwards})
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
        for element in attributes:
            params.update({element: attributes[element]})
        api_response = self.api_request('mail.set', params)
        return api_response

    def mail_delete(self, mail: str) -> dict:
        """
        Function to delete a mail
        :param mail: the mail to delete
        :return: the response for the request
        """
        api_response = self.api_request('mail.delete', {'mail':mail})
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

    def mail_apppassword_delete(self, id: int) -> dict:
        """
        Function to delete a mail app password
        :param id: the id of the mail app password
        :return: the response for the request
        """
        api_response = self.api_request('mail.apppassword.delete', {'id':id})
        return api_response
