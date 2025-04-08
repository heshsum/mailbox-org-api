from mailbox_org_api import Invoice
import unittest

test_account = 'test_account'
test_id = 'BMBO-1234-2025'

class TestMail(unittest.TestCase):

    def test_invoice_create(self):
        invoice = Invoice.Invoice(test_account, test_id)
        self.assertEqual(invoice.account, test_account)
        self.assertEqual(invoice.invoice_id, test_id)

    def test_invoice_account(self):
        invoice = Invoice.Invoice(test_account, test_id)
        self.assertEqual(invoice.account, test_account)
        account = 'test_account2'
        invoice.account = account
        self.assertEqual(invoice.account, account)

    def test_invoice_id(self):
        invoice = Invoice.Invoice(test_account, test_id)
        self.assertEqual(invoice.invoice_id, test_id)
        id = 'BMBO-9876-25'
        invoice.invoice_id = id
        self.assertEqual(invoice.invoice_id, id)

    def test_invoice_status(self):
        invoice = Invoice.Invoice(test_account, test_id)
        self.assertEqual(invoice.status, None)
        status = 'open'
        invoice.status = status
        self.assertEqual(invoice.status, status)

    def test_invoice_date(self):
        invoice = Invoice.Invoice(test_account, test_id)
        self.assertEqual(invoice.date, None)
        date = '2025-12-31'
        invoice.date = date
        self.assertEqual(invoice.date, date)

    def test_invoice_token(self):
        invoice = Invoice.Invoice(test_account, test_id)
        self.assertEqual(invoice.token, None)
        token = '123456789'
        invoice.token = token
        self.assertEqual(invoice.token, token)