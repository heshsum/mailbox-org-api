from mailbox_org_api import Account

account_name = 'heiner.hansen'

class TestAccount:
    def test_account(self):
        account = Account.Account(account_name)
        assert account.name == account_name

    def test_account_name(self):
        account = Account.Account(account_name)
        assert account.name == account_name
        test_name = 'tests'
        account.name = test_name
        assert account.name == test_name

    def test_account_account(self):
        account = Account.Account(account_name)
        assert account.account is None
        account_test = 'tests'
        account.account = account_test
        assert account.account == account_test

    def test_account_type(self):
        account = Account.Account(account_name)
        assert account.type is None
        account_type = 'test_type'
        account.type = account_type
        assert account.type == account_type

    def test_account_status(self):
        account = Account.Account(account_name)
        assert account.status is None
        status = 'aktiv'
        account.status = status
        assert account.status == status

    def test_account_language(self):
        account = Account.Account(account_name)
        assert account.language is None
        language = 'en_EN'
        account.language = language
        assert account.language == language

    def test_account_company(self):
        account = Account.Account(account_name)
        assert account.company is None
        company = 'test_company'
        account.company = company
        assert account.company == company

    def test_account_ustid(self):
        account = Account.Account(account_name)
        assert account.ustid is None
        ustid = 'test_ustid'
        account.ustid = ustid
        assert account.ustid == ustid

    def test_account_address_main(self):
        account = Account.Account(account_name)
        assert account.address_main == {}
        address_main = 'test_address_main'
        account.address_main = address_main
        assert account.address_main == address_main

    def test_account_address_payment(self):
        account = Account.Account(account_name)
        assert account.address_payment == {}
        address_payment = 'test_address_payment'
        account.address_payment = address_payment
        assert account.address_payment == address_payment

    def test_account_bank(self):
        account = Account.Account(account_name)
        assert account.bank == {}
        bank = {'iban': 'DE02120300000000202051', 'bic': 'BYLADEM1001', 'account_owner': 'Test', 'name': 'Test'}
        account.bank = bank
        assert account.bank == bank

    def test_account_contact(self):
        account = Account.Account(account_name)
        assert account.contact == {}
        contact = {'mail':'contact@tests.internal', 'first_name': 'Test', 'last_name': 'Contact', 'birthday': '',
                   'street':'Teststr. 1', 'zipcode':'12345', 'town':'Testtown', 'country':'DE'}
        account.contact = contact
        assert account.contact == contact

    def test_account_monthly_fee(self):
        account = Account.Account(account_name)
        assert account.monthly_fee is None
        monthly_fee = 'test_monthly_fee'
        account.monthly_fee = monthly_fee
        assert account.monthly_fee == monthly_fee

    def test_account_invoice_type(self):
        account = Account.Account(account_name)
        assert account.invoice_type is None
        invoice_type = 'test_invoice_type'
        account.invoice_type = invoice_type
        assert account.invoice_type == invoice_type

    def test_account_av_contract(self):
        account = Account.Account(account_name)
        assert account.av_contract == {}
        av_contract = {'signed': False}
        account.av_contract = av_contract
        assert account.av_contract == av_contract

    def test_account_tarifflimits(self):
        account = Account.Account(account_name)
        assert account.tarifflimits == {}
        tarifflimits = 'test_tarifflimits'
        account.tarifflimits = tarifflimits
        assert account.tarifflimits == tarifflimits

    def test_account_dta_allowed(self):
        account = Account.Account(account_name)
        assert account.dta_allowed is None
        dta_allowed = 'test_dta_allowed'
        account.dta_allowed = dta_allowed
        assert account.dta_allowed, dta_allowed

    def test_account_old_customer(self):
        account = Account.Account(account_name)
        assert account.old_customer is None
        old_customer = 'test_old_customer'
        account.old_customer = old_customer
        assert account.old_customer, old_customer

    def test_account_plan(self):
        account = Account.Account(account_name)
        assert account.plan is None
        plan = 'test_plan'
        account.plan = plan
        assert account.plan == plan

    def test_account_payment_type(self):
        account = Account.Account(account_name)
        assert account.payment_type is None
        payment_type = 'test_payment_type'
        account.payment_type = payment_type
        assert account.payment_type == payment_type
