import pytest
from mailbox_org_api import APIClient, Mail

def test_headers():
    client = APIClient.APIClient()
    assert client.auth_id is None
    assert client.level is None
    assert client.jsonrpc_id == 0

def test_hello_world():
    client = APIClient.APIClient()
    assert client.jsonrpc_id == 0
    assert client.hello_world() == 'Hello World!'
    assert client.jsonrpc_id == 1

mail_address = 'test@test.test'
def test_mail_object():
    mail = Mail.Mail(mail_address)
    assert mail.mail == mail_address

def test_mail_alternate_mail():
    mail = Mail.Mail(mail_address)
    alternate_mail = 'alternate_test@test.test'
    mail.alternate_mail = alternate_mail
    assert mail.alternate_mail == alternate_mail

def test_mail_phone():
    mail = Mail.Mail(mail_address)
    phone = '12345'
    mail.phone = phone
    assert mail.phone == phone

def test_mail_password():
    mail = Mail.Mail(mail_address)
    password = 'alligator9'
    mail.password = password
    assert mail.password == password

def test_mail_mail_quota():
    mail = Mail.Mail(mail_address)
    quota = 10
    mail.additional_mail_quota = quota
    assert mail.additional_mail_quota == quota

def test_mail_cloud_quota():
    mail = Mail.Mail(mail_address)
    quota = 10
    mail.additional_cloud_quota = quota
    assert mail.additional_cloud_quota == quota

def test_mail_aliases():
    mail = Mail.Mail(mail_address)
    mail1 = 'test1@test.test'
    mail2 = 'test2@test.test'
    aliases = [mail1, mail2]
    mail.aliases = aliases
    assert mail.aliases == aliases

def test_mail_plan():
    mail = Mail.Mail(mail_address)
    plan = 'standard'
    mail.plan = plan
    assert mail.plan == plan

def test_mail_same_password_allowed():
    mail = Mail.Mail(mail_address)
    same_password_allowed = True
    mail.same_password_allowed = same_password_allowed
    assert mail.same_password_allowed == True

def test_mail_active():
    mail = Mail.Mail(mail_address)
    mail.active = True
    assert mail.active == True

def test_mail_uid_extern():
    mail = Mail.Mail(mail_address)
    uid_extern = '12345'
    mail.uid_extern = uid_extern
    assert mail.uid_extern == uid_extern

def test_mail_allow_nets():
    mail = Mail.Mail(mail_address)
    allow_nets = ['1.1.1.1', '2.2.2.2']
    mail.allow_nets = allow_nets
    assert mail.allow_nets == allow_nets

def test_mail_birthday():
    mail = Mail.Mail(mail_address)
    birthday = '1980-12-31'
    mail.birthday = birthday
    assert mail.birthday == birthday

def test_mail_capabilities():
    mail = Mail.Mail(mail_address)
    capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST']
    mail.capabilities = capabilities
    assert mail.capabilities == capabilities

def test_mail_cell_phone():
    mail = Mail.Mail(mail_address)
    cell_phone = '12345'
    mail.cell_phone = cell_phone
    assert mail.cell_phone == cell_phone

def test_mail_city():
    mail = Mail.Mail(mail_address)
    city = 'Berlin'
    mail.city = city
    assert mail.city == city
