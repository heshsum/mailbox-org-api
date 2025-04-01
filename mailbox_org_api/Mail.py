from datetime import datetime


class Mail:
    def __init__(self, mail: str):
        self.mail = mail
        self.password = None
        self.password_hash = None
        self.same_password_allowed = None
        self.require_password_reset = None
        self.plan = None
        self.additional_mail_quota = None
        self.additional_cloud_quota = None
        self.first_name = None
        self.last_name = None
        self.inboxsave = None
        self.forwards = None
        self.aliases = None
        self.alternate_mail = None
        self.memo = None
        self.allow_nets = None
        self.active = None
        self.title = None
        self.birthday = None
        self.position = None
        self.department = None
        self.company = None
        self.street = None
        self.postal_code = None
        self.city = None
        self.phone = None
        self.fax = None
        self.cell_phone = None
        self.uid_extern = None
        self.language = None
        self.capabilities = None
        self.creation_date = None

        @property
        def mail(self) -> str:
            return self._mail

        @mail.setter
        def mail(self, mail: str):
            self._mail = mail

        @property
        def password(self) -> str:
            return self._password

        @password.setter
        def password(self, password: str):
            self._password = password

        @property
        def password_hash(self) -> str:
            return self._password_hash

        @password_hash.setter
        def password_hash(self, password_hash: str):
            self._password_hash = password_hash

        @property
        def same_password_allowed(self) -> bool:
            return self._same_password_allowed

        @same_password_allowed.setter
        def same_password_allowed(self, same_password_allowed: bool):
            self._same_password_allowed = same_password_allowed

        @property
        def require_password_reset(self) -> bool:
            return self._require_password_reset

        @require_password_reset.setter
        def require_password_reset(self, require_password_reset: bool):
            self._require_password_reset = require_password_reset

        @property
        def plan(self) -> str:
            return self._plan

        @plan.setter
        def plan(self, plan: str):
            self._plan = plan

        @property
        def additional_mail_quota(self) -> int:
            return self._additional_mail_quota

        @additional_mail_quota.setter
        def additional_mail_quota(self, additional_mail_quota: int):
            self._additional_mail_quota = additional_mail_quota

        @property
        def additional_cloud_quota(self) -> int:
            return self._additional_cloud_quota

        @additional_cloud_quota.setter
        def additional_cloud_quota(self, additional_cloud_quota: int):
            self._additional_cloud_quota = additional_cloud_quota

        @property
        def first_name(self) -> str:
            return self._first_name

        @first_name.setter
        def first_name(self, first_name: str):
            self._first_name = first_name

        @property
        def last_name(self) -> str:
            return self._last_name

        @last_name.setter
        def last_name(self, last_name: str):
            self._last_name = last_name

        @property
        def inboxsave(self) -> bool:
            return self._inboxsave

        @inboxsave.setter
        def inboxsave(self, inboxsave: bool):
            self._inboxsave = inboxsave

        @property
        def forwards(self) -> list:
            return self._forwards

        @forwards.setter
        def forwards(self, forwards: list):
            self._forwards = forwards

        @property
        def aliases(self) -> list:
            return self._aliases

        @aliases.setter
        def aliases(self, aliases: list):
            self._aliases = aliases

        @property
        def alternate_mail(self) -> str:
            return self._alternate_mail

        @alternate_mail.setter
        def alternate_mail(self, alternate_mail: str):
            # mail.set uses a String for this!
            self._alternate_mail = alternate_mail

        @property
        def allow_nets(self) -> list:
            return self._allow_nets

        @allow_nets.setter
        def allow_nets(self, allow_nets: list):
            self._allow_nets = allow_nets

        @property
        def active(self) -> bool:
            return self._active

        @active.setter
        def active(self, active: bool):
            self._active = active

        @property
        def title(self) -> str:
            return self._title

        @title.setter
        def title(self, title: str):
            self._title = title

        @property
        def birthday(self) -> str:
            return self._birthday

        @birthday.setter
        def birthday(self, birthday: str):
            self._birthday = birthday

        @property
        def position(self) -> str:
            return self._position

        @position.setter
        def position(self, position: str):
            self._position = position

        @property
        def department(self) -> str:
            return self._department

        @department.setter
        def department(self, department: str):
            self._department = department

        @property
        def company(self) -> str:
            return self._company

        @company.setter
        def company(self, company: str):
            self._company = company

        @property
        def street(self) -> str:
            return self._street

        @street.setter
        def street(self, street: str):
            self._street = street

        @property
        def postal_code(self) -> str:
            return self._postal_code

        @postal_code.setter
        def postal_code(self, postal_code: str):
            self._postal_code = postal_code

        @property
        def city(self) -> str:
            return self._city

        @city.setter
        def city(self, city: str):
            self._city = city

        @property
        def phone(self) -> str:
            return self._phone

        @phone.setter
        def phone(self, phone: str):
            self._phone = phone

        @property
        def fax(self) -> str:
            return self._fax

        @fax.setter
        def fax(self, fax: str):
            self._fax = fax

        @property
        def cell_phone(self) -> str:
            return self._cell_phone

        @cell_phone.setter
        def cell_phone(self, cell_phone: str):
            self._cell_phone = cell_phone

        @property
        def uid_extern(self) -> str:
            return self._uid_extern

        @uid_extern.setter
        def uid_extern(self, uid_extern: str):
            self._uid_extern = uid_extern

        @property
        def language(self) -> str:
            return self._language

        @language.setter
        def language(self, language: str):
            self._language = language

        @property
        def capabilities(self) -> list:
            return self._capabilities

        @capabilities.setter
        def capabilities(self, capabilities: list):
            self._capabilities = capabilities

        @property
        def creation_date(self) -> str:
            return self._creation_date

        @creation_date.setter
        def creation_date(self, creation_date: str):
            self._creation_date = creation_date

    def __str__(self):
        str = ""
        for attr in dir(self):
            str.join("obj.%s = %r" % (attr, getattr(self, attr)))
        return str