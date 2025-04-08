class Invoice:
    def __init__(self, account: str, invoice_id: str):
        self._account = account
        self._invoice_id = invoice_id
        self._status = None
        self._date = None
        self._token = None

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, account: str):
        self._account = account

    @property
    def invoice_id(self):
        return self._invoice_id

    @invoice_id.setter
    def invoice_id(self, id: str):
        self._invoice_id = id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: str):
        self._status = status

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date: str):
        self._date = date

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    def __str__(self) -> str:
        print_string = ''
        # Get object attributes as a dict in order to iterate
        for k, v in self.__dict__.items():
            # Add each attribute to the String.
            # As the attribute name is '_attribute', remove the leading character
            print_string += f'{k[1:]}: {v}\n'
        return print_string