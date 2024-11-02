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
        print('Request:', request)

        api_response = requests.post(
            self.url, data=json.dumps(request), headers=headers).json()
        print('API response:', api_response)
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

    def domain_list(self, account) -> dict:
        """
        Function to list all domains
        :param account: the account to list domains for
        :return: the API response
        """
        api_response = self.api_request('domain_list',{'account':account})
        return api_response

    def mail_list(self, domain) -> dict:
        """
        Function to list all mailboxes
        :return: the response from the mailbox.org Business API
        """
        api_response = self.api_request('mail.list', {'domain':domain})
        return api_response


    def mail_get(self, mail: str):
        """
        Function to retrieve a mail address
        :param mail: the mail to retrieve
        :return the response for the request
        """
        api_response = self.api_request('mail_get', {'mail':mail})
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
        api_response = self.api_request('mail_add',{'mail':mail, 'password':password, 'plan':plan,
                                                    'first_name':first_name, 'last_name':last_name,
                                                    'inboxsave':inboxsave, 'forwards':forwards})
        return api_response

    def mail_delete(self, mail: str):
        """
        Function to delete a mail
        :param mail: the mail to delete
        :return: the response for the request
        """
        api_response = self.api_request('mail_delete', {'mail':mail})
        return api_response