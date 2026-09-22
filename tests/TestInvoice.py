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
        assert invoice.invoice_id == id

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

    def test_invoice_csv(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.csv is None
        csv_data = 'date,services,description,quantity,currency,net,vat_percent,total'
        invoice.csv = csv_data
        assert invoice.csv == csv_data

    def test_invoice_pdf(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.pdf is None
        pdf_data = '%PDF-1.7'
        invoice.pdf = pdf_data
        assert invoice.pdf == pdf_data

    def test_invoice_xml(self):
        invoice = Invoice.Invoice(test_account, test_id)
        assert invoice.xml is None
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        invoice.xml = xml_data
        assert invoice.xml == xml_data

    def test_invoice_str(self):
        invoice = Invoice.Invoice(test_account, test_id)
        result_str = str(invoice)
        assert f'account: {test_account}' in result_str
        assert f'invoice_id: {test_id}' in result_str

