from dataclasses import dataclass, asdict


@dataclass
class Invoice:
    account: str
    invoice_id: str
    status: str | None = None
    date: str | None = None
    token: str | None = None
    csv: str | None = None
    pdf: str | None = None
    xml: str | None = None

    def __str__(self) -> str:
        return ''.join(f"{k}: {v}\n" for k, v in asdict(self).items())
