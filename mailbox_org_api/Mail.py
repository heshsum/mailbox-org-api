from dataclasses import dataclass, field, asdict


@dataclass
class Mail:
    mail: str
    password: str | None = None
    password_hash: str | None = None
    same_password_disallowed: bool | None = None
    require_reset_password: bool | None = None
    plan: str | None = None
    additional_mail_quota: int | None = None
    additional_cloud_quota: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    inboxsave: bool | None = None
    forwards: list | None = None
    aliases: list | None = None
    alternate_mail: str | None = None  # mail.set uses a String for this!
    memo: str | None = None
    allow_nets: list | None = None
    active: bool | None = None
    title: str | None = None
    birthday: str | None = None
    position: str | None = None
    department: str | None = None
    company: str | None = None
    street: str | None = None
    postal_code: str | None = None
    city: str | None = None
    phone: str | None = None
    fax: str | None = None
    cell_phone: str | None = None
    uid_extern: str | None = None
    language: str | None = None
    capabilities: list | None = None
    creation_date: str | None = None
    uid: str | None = None
    type: str | None = None
    plansavailable: list = field(default_factory=list)

    def __str__(self) -> str:
        return ''.join(f"{k}: {v}\n" for k, v in asdict(self).items())
