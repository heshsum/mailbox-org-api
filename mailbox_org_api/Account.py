from dataclasses import dataclass, field, asdict


@dataclass
class Account:
    name: str
    account: str | None = None
    type: str | None = None
    status: str | None = None
    plan: str | None = None
    old_customer: bool | None = None
    language: str | None = None
    company: str | None = None
    ustid: str | None = None
    address_main: dict = field(default_factory=dict)
    address_payment: dict = field(default_factory=dict)
    bank: dict = field(default_factory=dict)
    contact: dict = field(default_factory=dict)
    monthly_fee: float | None = None
    invoice_type: str | None = None
    av_contract: dict = field(default_factory=dict)
    tarifflimits: dict = field(default_factory=dict)
    dta_allowed: bool | None = None
    payment_type: str | None = None

    def __str__(self) -> str:
        return ''.join(f"{k}: {v}\n" for k, v in asdict(self).items())
