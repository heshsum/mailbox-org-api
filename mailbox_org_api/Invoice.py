class Invoice:
    def __init__(self, account: str, invoice_id: str):
        self._account = account
        self._invoice_id = invoice_id
        self._status = None
        self._date = None
        self._token = None
        self._csv = None
        self._pdf = None
        self._xml = None

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
    def invoice_id(self, invoice_id: str):
        self._invoice_id = invoice_id

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

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, csv: str):
        self._csv = csv

    @property
    def pdf(self):
        return self._pdf

    @pdf.setter
    def pdf(self, pdf: str):
        self._pdf = pdf

    @property
    def xml(self):
        return self._xml

    @xml.setter
    def xml(self, xml: str):
        self._xml = xml

    def __str__(self) -> str:
        print_string = ''
        # Get object attributes as a dict in order to iterate
        for k, v in self.__dict__.items():
            # Add each attribute to the String.
            # As the attribute name is '_attribute', remove the leading character
            print_string += f'{k[1:]}: {v}\n'
        return print_string