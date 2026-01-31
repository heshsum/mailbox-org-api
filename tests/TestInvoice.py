from mailbox_org_api import Invoice

test_account = 'test_account'
test_id = 'BMBO-1234-2025'

class TestMail:

    def test_invoice_create(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.account == test_account
        assert invoice.invoice_id == test_id

    def test_invoice_account(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.account == test_account
        account = 'test_account2'
        invoice.account = account
        assert invoice.account == account

    def test_invoice_id(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.invoice_id == test_id
        id = 'BMBO-9876-25'
        invoice.invoice_id = id
        assert invoice.invoice_id, id

    def test_invoice_status(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.status is None
        status = 'open'
        invoice.status = status
        assert invoice.status == status

    def test_invoice_date(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.date is None
        date = '2025-12-31'
        invoice.date = date
        assert invoice.date == date

    def test_invoice_token(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.token is None
        token = '123456789'
        invoice.token = token
        assert invoice.token == token