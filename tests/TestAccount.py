from mailbox_org_api import Account
import unittest

account_name = 'heiner.hansen'


class TestAccount(unittest.TestCase):

    def test_account(self):
        account = Account.Account(account_name)
        self.assertEqual(account.name, account_name)

    def test_account_name(self):
        account = Account.Account(account_name)
        self.assertEqual(account.name, account_name)
        test_name = 'tests'
        account.name = test_name
        self.assertEqual(account.name, test_name)

    def test_account_account(self):
        account = Account.Account(account_name)
        self.assertEqual(account.account, None)
        account_test = 'tests'
        account.account = account_test
        self.assertEqual(account.account, account_test)

    def test_account_type(self):
        account = Account.Account(account_name)
        self.assertEqual(account.type, None)
        accouunt_type = 'test_type'
        account.type = accouunt_type
        self.assertEqual(account.type, accouunt_type)

    def test_account_status(self):
        account = Account.Account(account_name)
        self.assertEqual(account.status, None)
        status = 'aktiv'
        account.status = status
        self.assertEqual(account.status, status)

    def test_account_language(self):
        account = Account.Account(account_name)
        self.assertEqual(account.language, None)
        language = 'en_EN'
        account.language = language
        self.assertEqual(account.language, language)

    def test_account_company(self):
        account = Account.Account(account_name)
        self.assertEqual(account.company, None)
        company = 'test_company'
        account.company = company
        self.assertEqual(account.company, company)

    def test_account_ustid(self):
        account = Account.Account(account_name)
        self.assertEqual(account.ustid, None)
        ustid = 'test_ustid'
        account.ustid = ustid
        self.assertEqual(account.ustid, ustid)

    def test_account_address_main(self):
        account = Account.Account(account_name)
        self.assertEqual(account.address_main, {})
        address_main = 'test_address_main'
        account.address_main = address_main
        self.assertEqual(account.address_main, address_main)

    def test_account_address_payment(self):
        account = Account.Account(account_name)
        self.assertEqual(account.address_payment, {})
        address_payment = 'test_address_payment'
        account.address_payment = address_payment
        self.assertEqual(account.address_payment, address_payment)

    def test_account_bank(self):
        account = Account.Account(account_name)
        self.assertEqual(account.bank, {})
        bank = {'iban': 'DE02120300000000202051', 'bic': 'BYLADEM1001', 'account_owner': 'Test', 'name': 'Test'}
        account.bank = bank
        self.assertEqual(account.bank, bank)

    def test_account_contact(self):
        account = Account.Account(account_name)
        self.assertEqual(account.contact, {})
        contact = {'mail':'contact@tests.internal', 'first_name': 'Test', 'last_name': 'Contact', 'birthday': '',
                   'street':'Teststr. 1', 'zipcode':'12345', 'town':'Testtown', 'country':'DE'}
        account.contact = contact
        self.assertEqual(account.contact, contact)

    def test_account_monthly_fee(self):
        account = Account.Account(account_name)
        self.assertEqual(account.monthly_fee, None)
        monthly_fee = 'test_monthly_fee'
        account.monthly_fee = monthly_fee
        self.assertEqual(account.monthly_fee, monthly_fee)

    def test_account_invoice_type(self):
        account = Account.Account(account_name)
        self.assertEqual(account.invoice_type, None)
        invoice_type = 'test_invoice_type'
        account.invoice_type = invoice_type
        self.assertEqual(account.invoice_type, invoice_type)

    def test_account_av_contract(self):
        account = Account.Account(account_name)
        self.assertEqual(account.av_contract, {})
        av_contract = {'signed': False}
        account.av_contract = av_contract
        self.assertEqual(account.av_contract, av_contract)

    def test_account_tarifflimits(self):
        account = Account.Account(account_name)
        self.assertEqual(account.tarifflimits, {})
        tarifflimits = 'test_tarifflimits'
        account.tarifflimits = tarifflimits
        self.assertEqual(account.tarifflimits, tarifflimits)

    def test_account_dta_allowed(self):
        account = Account.Account(account_name)
        self.assertEqual(account.dta_allowed, None)
        dta_allowed = 'test_dta_allowed'
        account.dta_allowed = dta_allowed
        self.assertEqual(account.dta_allowed, dta_allowed)

    def test_account_old_customer(self):
        account = Account.Account(account_name)
        self.assertEqual(account.old_customer, None)
        old_customer = 'test_old_customer'
        account.old_customer = old_customer
        self.assertEqual(account.old_customer, old_customer)

    def test_account_plan(self):
        account = Account.Account(account_name)
        self.assertEqual(account.plan, None)
        plan = 'test_plan'
        account.plan = plan
        self.assertEqual(account.plan, plan)

    def test_account_payment_type(self):
        account = Account.Account(account_name)
        self.assertEqual(account.payment_type, None)
        payment_type = 'test_payment_type'
        account.payment_type = payment_type
        self.assertEqual(account.payment_type, payment_type)

if __name__ == '__main__':
    unittest.main()
