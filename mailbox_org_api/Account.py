class Account:
    def __init__(self, name: str):
        self._name = name
        self._account = None
        self._type = None
        self._status = None
        self._language = None
        self._company = None
        self._ustid = None
        self._address_main = {}
        self._address_payment = {}
        self._bank = {}
        self._contact = {}
        self._monthly_fee = None
        self._invoice_type = None
        self._av_contract = {}
        self._tarifflimits = {}
        self._dta_allowed = None
        self._old_customer = None
        self._plan = None
        self._payment_type = None

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name: str):
        self._name = name
    @property
    def account(self):
        return self._account
    @account.setter
    def account(self, account: str):
        self._account = account
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, account_type: str):
        self._type = account_type
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status: str):
        self._status = status
    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, language: str):
        self._language = language
    @property
    def company(self):
        return self._company
    @company.setter
    def company(self, company: str):
        self._company = company
    @property
    def ustid(self):
        return self._ustid
    @ustid.setter
    def ustid(self, ustid: str):
        self._ustid = ustid
    @property
    def address_main(self):
        return self._address_main

    @address_main.setter
    def address_main(self, address_main: dict):
        self._address_main = address_main

    @property
    def address_payment(self):
        return self._address_payment

    @address_payment.setter
    def address_payment(self, address_payment: dict):
        self._address_payment = address_payment

    @property
    def bank(self):
        return self._bank

    @bank.setter
    def bank(self, bank: dict):
        self._bank = bank

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, contact: dict):
        self._contact = contact

    @property
    def monthly_fee(self):
        return self._monthly_fee
    @monthly_fee.setter
    def monthly_fee(self, monthly_fee: float):
        self._monthly_fee = monthly_fee
    @property
    def invoice_type(self):
        return self._invoice_type
    @invoice_type.setter
    def invoice_type(self, invoice_type: str):
        self._invoice_type = invoice_type
    @property
    def av_contract(self):
        return self._av_contract
    @av_contract.setter
    def av_contract(self, av_contract: dict):
        self._av_contract = av_contract

    @property
    def tarifflimits(self):
        return self._tarifflimits

    @tarifflimits.setter
    def tarifflimits(self, tarifflimits: list):
        self._tarifflimits = tarifflimits

    @property
    def dta_allowed(self):
        return self._dta_allowed

    @dta_allowed.setter
    def dta_allowed(self, dta_allowed: bool):
        self._dta_allowed = dta_allowed

    @property
    def old_customer(self):
        return self._old_customer

    @old_customer.setter
    def old_customer(self, old_customer: bool):
        self._old_customer = old_customer

    @property
    def plan(self):
        return self._plan

    @plan.setter
    def plan(self, plan: str):
        self._plan = plan

    @property
    def payment_type(self):
        return self._payment_type

    @payment_type.setter
    def payment_type(self, payment_type: str):
        self._payment_type = payment_type


    def __str__(self) -> str:
        print_string = ''
        # Get object attributes as a dict in order to iterate
        for k, v in self.__dict__.items():
            # Add each attribute to the String.
            # As the attribute name is '_attribute', remove the leading character
            print_string += f'{k[1:]}: {v}\n'
        return print_string