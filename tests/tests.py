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
def test_mail_address():
    mail = Mail.Mail(mail_address)
    assert mail.mail == mail_address

def test_mail_password():
    mail = Mail.Mail(mail_address)
    password = 'alligator9'
    mail.password = password
    assert mail.password == password

def test_mail_password_hash():
    mail = Mail.Mail(mail_address)
    password_hash = '{SSHA}hdF+6b0xKmkWNZfHrVfUlWqo10M7nje6'
    mail.password_hash = password_hash
    assert mail.password_hash == password_hash

def test_mail_same_password_allowed():
    mail = Mail.Mail(mail_address)
    same_password_allowed = True
    mail.same_password_allowed = same_password_allowed
    assert mail.same_password_allowed == True

def test_mail_require_password_reset():
    mail = Mail.Mail(mail_address)
    require_password_reset = True
    mail.require_password_reset = require_password_reset
    assert mail.require_password_reset == require_password_reset

def test_mail_plan():
    mail = Mail.Mail(mail_address)
    plan = 'standard'
    mail.plan = plan
    assert mail.plan == plan

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

def test_mail_first_name():
    mail = Mail.Mail(mail_address)
    first_name = 'test first name'
    mail.first_name = first_name
    assert mail.first_name == first_name

def test_mail_last_name():
    mail = Mail.Mail(mail_address)
    last_name = 'test'
    mail.last_name = last_name
    assert mail.last_name == last_name

def test_mail_inboxsave():
    mail = Mail.Mail(mail_address)
    inboxsave = True
    mail.inboxsave = inboxsave
    assert mail.inboxsave == inboxsave

def test_mail_forwards():
    mail = Mail.Mail(mail_address)
    forwards = ['mail1@test.internal', 'mail2@test.internal', 'mail3@test.internal']
    mail.forwards = forwards
    assert mail.forwards == forwards

def test_mail_aliases():
    mail = Mail.Mail(mail_address)
    aliases = ['mail1@test.internal', 'mail2@test.internal', 'mail3@test.internal']
    mail.aliases = aliases
    assert mail.aliases == aliases

def test_mail_alternate_mail():
    mail = Mail.Mail(mail_address)
    alternate_mail = 'alternate_test@test.test'
    mail.alternate_mail = alternate_mail
    assert mail.alternate_mail == alternate_mail

def test_mail_memo():
    mail = Mail.Mail(mail_address)
    memo = 'test'
    mail.memo = memo
    assert mail.memo == memo

def test_mail_allow_nets():
    mail = Mail.Mail(mail_address)
    allow_nets = ['192.168.0.0/24', '192.168.127.12/24', '172.16.31.10/24']
    mail.allow_nets = allow_nets
    assert mail.allow_nets == allow_nets

def test_mail_active():
    mail = Mail.Mail(mail_address)
    active = True
    mail.active = active
    assert mail.active == active

def test_mail_title():
    mail = Mail.Mail(mail_address)
    title = 'test'
    mail.title = title
    assert mail.title == title

def test_mail_birthday():
    mail = Mail.Mail(mail_address)
    birthday = '1980-12-31'
    mail.birthday = birthday
    assert mail.birthday == birthday

def test_mail_position():
    mail = Mail.Mail(mail_address)
    position = 'test position'
    mail.position = position
    assert mail.position == position

def test_mail_department():
    mail = Mail.Mail(mail_address)
    department = 'test department'
    mail.department = department
    assert mail.department == department

def test_mail_company():
    mail = Mail.Mail(mail_address)
    company = 'test company'
    mail.company = company
    assert mail.company == company

def test_mail_street():
    mail = Mail.Mail(mail_address)
    street = 'test street 1'
    mail.street = street
    assert mail.street == street

def test_mail_postal_code():
    mail = Mail.Mail(mail_address)
    postal_code = 'test postal code 12345'
    mail.postal_code = postal_code
    assert mail.postal_code == postal_code

def test_mail_city():
    mail = Mail.Mail(mail_address)
    city = 'test city'
    mail.city = city
    assert mail.city == city

def test_mail_phone():
    mail = Mail.Mail(mail_address)
    phone = '+493012345'
    mail.phone = phone
    assert mail.phone == phone

def test_mail_fax():
    mail = Mail.Mail(mail_address)
    fax = '+493012345'
    mail.fax = fax
    assert mail.fax == fax

def test_mail_cell_phone():
    mail = Mail.Mail(mail_address)
    cell_phone = '12345'
    mail.cell_phone = cell_phone
    assert mail.cell_phone == cell_phone

def test_mail_uid_extern():
    mail = Mail.Mail(mail_address)
    uid_extern = 'test uid extern'
    mail.uid_extern = uid_extern
    assert mail.uid_extern == uid_extern

def test_mail_language():
    mail = Mail.Mail(mail_address)
    language = 'en_EN'
    mail.language = language
    assert mail.language == language

def test_mail_capabilities():
    mail = Mail.Mail(mail_address)
    capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST']
    mail.capabilities = capabilities
    assert mail.capabilities == capabilities

def test_mail_creation_date():
    mail = Mail.Mail(mail_address)
    creation_date = '1980-12-31 00:00:00'
    mail.creation_date = creation_date
    assert mail.creation_date == creation_date

def test_mail_uid():
    mail = Mail.Mail(mail_address)
    uid = 'test uid'
    mail.uid = uid
    assert mail.uid == uid

def test_mail_type():
    mail = Mail.Mail(mail_address)
    type = 'inbox'
    mail.type = type
    assert mail.type == type

def test_mail_plansavailable():
    mail = Mail.Mail(mail_address)
    plansavailable = ['light', 'standard', 'premium']
    mail.plansavailable = plansavailable
    assert mail.plansavailable == plansavailable