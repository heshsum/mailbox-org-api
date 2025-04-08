from mailbox_org_api import Mail
import unittest

mail_address = 'tests@tests.tests'

class TestMail(unittest.TestCase):

    def test_init(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.mail, mail_address)

    def test_mail_address(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.mail, mail_address)
        test_address = 'test2@tests.tests'
        mail.mail = test_address
        self.assertEqual(mail.mail, test_address)

    def test_mail_password(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.password, None)
        password = 'Alligator9'
        mail.password = password
        self.assertEqual(mail.password, password)

    def test_mail_password_hash(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.password_hash, None)
        password_hash = '{SSHA}hdF+6b0xKmkWNZfHrVfUlWqo10M7nje6'
        mail.password_hash = password_hash
        self.assertEqual(mail.password_hash, password_hash)

    def test_mail_same_password_allowed(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.same_password_allowed, None)
        same_password_allowed = True
        mail.same_password_allowed = same_password_allowed
        self.assertTrue(mail.same_password_allowed)

    def test_mail_require_password_reset(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.require_password_reset, None)
        require_password_reset = True
        mail.require_password_reset = require_password_reset
        self.assertTrue(mail.require_password_reset)

    def test_mail_plan(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.plan, None)
        plan = 'standard'
        mail.plan = plan
        self.assertEqual(mail.plan, plan)

    def test_mail_mail_quota(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.additional_mail_quota, None)
        quota = 10
        mail.additional_mail_quota = quota
        self.assertEqual(mail.additional_mail_quota, quota)

    def test_mail_cloud_quota(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.additional_cloud_quota, None)
        quota = 10
        mail.additional_cloud_quota = quota
        self.assertEqual(mail.additional_cloud_quota, quota)

    def test_mail_first_name(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.first_name, None)
        first_name = 'test first name'
        mail.first_name = first_name
        self.assertEqual(mail.first_name, first_name)

    def test_mail_last_name(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.last_name, None)
        last_name = 'test'
        mail.last_name = last_name
        self.assertEqual(mail.last_name, last_name)

    def test_mail_inboxsave(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.inboxsave, None)
        inboxsave = True
        mail.inboxsave = inboxsave
        self.assertEqual(mail.inboxsave, inboxsave)

    def test_mail_forwards(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.forwards, None)
        forwards = ['mail1@test.internal', 'mail2@test.internal', 'mail3@test.internal']
        mail.forwards = forwards
        self.assertEqual(mail.forwards, forwards)

    def test_mail_aliases(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.aliases, None)
        aliases = ['mail1@test.internal', 'mail2@test.internal', 'mail3@test.internal']
        mail.aliases = aliases
        self.assertEqual(mail.aliases, aliases)

    def test_mail_alternate_mail(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.alternate_mail, None)
        alternate_mail = 'alternate_test@test.test'
        mail.alternate_mail = alternate_mail
        self.assertEqual(mail.alternate_mail, alternate_mail)

    def test_mail_memo(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.memo, None)
        memo = 'test'
        mail.memo = memo
        self.assertEqual(mail.memo, memo)

    def test_mail_allow_nets(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.allow_nets, None)
        allow_nets = ['192.168.0.0/24', '192.168.127.12/24', '172.16.31.10/24']
        mail.allow_nets = allow_nets
        self.assertEqual(mail.allow_nets, allow_nets)

    def test_mail_active(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.active, None)
        active = True
        mail.active = active
        self.assertEqual(mail.active, active)

    def test_mail_title(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.title, None)
        title = 'test'
        mail.title = title
        self.assertEqual(mail.title, title)

    def test_mail_birthday(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.birthday, None)
        birthday = '1980-12-31'
        mail.birthday = birthday
        self.assertEqual(mail.birthday, birthday)

    def test_mail_position(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.position, None)
        position = 'test position'
        mail.position = position
        self.assertEqual(mail.position, position)

    def test_mail_department(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.department, None)
        department = 'test department'
        mail.department = department
        self.assertEqual(mail.department, department)

    def test_mail_company(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.company, None)
        company = 'test company'
        mail.company = company
        self.assertEqual(mail.company, company)

    def test_mail_street(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.street, None)
        street = 'test street 1'
        mail.street = street
        self.assertEqual(mail.street, street)

    def test_mail_postal_code(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.postal_code, None)
        postal_code = 'test postal code 12345'
        mail.postal_code = postal_code
        self.assertEqual(mail.postal_code, postal_code)

    def test_mail_city(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.city, None)
        city = 'test city'
        mail.city = city
        self.assertEqual(mail.city, city)

    def test_mail_phone(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.phone, None)
        phone = '+493012345'
        mail.phone = phone
        self.assertEqual(mail.phone, phone)

    def test_mail_fax(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.fax, None)
        fax = '+493012345'
        mail.fax = fax
        self.assertEqual(mail.fax, fax)

    def test_mail_cell_phone(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.cell_phone, None)
        cell_phone = '12345'
        mail.cell_phone = cell_phone
        self.assertEqual(mail.cell_phone, cell_phone)

    def test_mail_uid_extern(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.uid_extern, None)
        uid_extern = 'test uid extern'
        mail.uid_extern = uid_extern
        self.assertEqual(mail.uid_extern, uid_extern)

    def test_mail_language(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.language, None)
        language = 'en_EN'
        mail.language = language
        self.assertEqual(mail.language, language)

    def test_mail_capabilities(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.capabilities, None)
        capabilities = ['MAIL_SPAMPROTECTION', 'MAIL_BLACKLIST']
        mail.capabilities = capabilities
        self.assertEqual(mail.capabilities, capabilities)

    def test_mail_creation_date(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.creation_date, None)
        creation_date = '1980-12-31 00:00:00'
        mail.creation_date = creation_date
        self.assertEqual(mail.creation_date, creation_date)

    def test_mail_uid(self):
        mail = Mail.Mail(mail_address)
        uid = 'test uid'
        mail.uid = uid
        self.assertEqual(mail.uid, uid)

    def test_mail_type(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.type, None)
        mail_type = 'inbox'
        mail.type = mail_type
        self.assertEqual(mail.type, mail_type)

    def test_mail_plansavailable(self):
        mail = Mail.Mail(mail_address)
        self.assertEqual(mail.plansavailable, [])
        plansavailable = ['light', 'standard', 'premium']
        mail.plansavailable = plansavailable
        self.assertEqual(mail.plansavailable, plansavailable)


if __name__ == '__main__':
    unittest.main()

account = 'test_account'
