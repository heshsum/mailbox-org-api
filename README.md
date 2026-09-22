[![Python Test](https://github.com/heshsum/mailbox-org-api/actions/workflows/python-test.yml/badge.svg?branch=main)](https://github.com/heshsum/mailbox-org-api/actions/workflows/python-test.yml)
[![PyPI version](https://img.shields.io/pypi/v/mailbox-org-api.svg)](https://pypi.org/project/mailbox-org-api/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mailbox-org-api.svg)](https://pypi.org/project/mailbox-org-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# mailbox-org-api

A Python library to access and automate the [mailbox.org Business API](https://api.mailbox.org).

The primary goal of this package is to mirror all calls and features of the official mailbox.org Business API while providing high-level helper functions and object-oriented abstractions for common administrative tasks.

> 📖 **Full Documentation**: Comprehensive documentation, method signatures, and guides are available on the [Project Wiki](https://github.com/heshsum/mailbox-org-api/wiki).

---

## Features

- **Direct API Mirroring**: Straightforward mapping of mailbox.org JSON-RPC methods using Pythonic naming (e.g. `mail.add` &rarr; `mail_add`).
- **Context Manager Support**: Clean session lifecycle handling via `with APIClient() as api:`, which automatically handles session termination (`deauth`) and connection cleanup.
- **Convenience Helpers**: High-level helpers for everyday tasks such as password management, force-reset on login, plan upgrades, aliases, forwarders, storage quotas, vacation autoresponders, and invoice downloads.
- **Object-Oriented Models**: Built-in models (`Mail`, `Account`, `Invoice`) for interacting with resources as Python objects.
- **Pre-flight Validation**: Parameter names and types are validated prior to sending API requests to catch typos early.
- **Automatic Retries**: Built-in exponential backoff for transient HTTP errors (e.g., 429, 500, 502, 503, 504).
- **Safe Debug Logging**: Optional request and response inspection with automatic redaction of sensitive credentials (passwords, tokens, auth keys).

---

## Installation

Requires **Python >= 3.11**.

### From PyPI
```bash
pip install mailbox-org-api
```

### From Source
```bash
pip install git+https://github.com/heshsum/mailbox-org-api.git
```

For more details on requirements and installation options, see the [Installation Wiki](https://github.com/heshsum/mailbox-org-api/wiki/1.-Installation).

---

## Quickstart

All API interactions start with an instance of `APIClient`. Using a context manager (`with`) is recommended to ensure your session is always de-authenticated and connections are properly closed when done.

```python
from mailbox_org_api.APIClient import APIClient
from mailbox_org_api.APIError import APIError

USERNAME = "YourAdminUsername"
PASSWORD = "YourSecretPassword"

# Initialize client and authenticate using a context manager
with APIClient() as api:
    # Authenticate to begin an API session
    api.auth(USERNAME, PASSWORD)
    print(f"Logged in! Access level: {api.level}")

    # Check connection
    api.hello_innerworld()

    # List all domains configured for this account
    domains = api.domain_get_list(USERNAME)
    print(f"Domains: {domains}")
```

> **Manual Session Management**: If not using a context manager, call `api.deauth()` when finished to close your session.
> 
> **Debug Mode**: Pass `debug_output=True` when creating the client (`APIClient(debug_output=True)`) to print all requests and responses with credentials safely redacted.
> 
> See the [Basic Usage Wiki](https://github.com/heshsum/mailbox-org-api/wiki/2.-Basic-usage) for details on naming conventions, validation, and return formats.

---

## Usage Examples

### 1. Managing Mailboxes (Inboxes)

The library provides both raw methods mirroring `mail.*` endpoints and convenient shortcuts for common mailbox operations.

For a full list of parameters and options, see [Mail Methods in the Wiki](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#mail).

```python
from mailbox_org_api.APIClient import APIClient

with APIClient() as api:
    api.auth("YourAdminUsername", "YourPassword")

    mail = "jane.doe@example.com"

    # 1. Create a new inbox
    api.mail_add(
        mail=mail,
        password="InitialPassword123!",
        plan="standard",
        first_name="Jane",
        last_name="Doe"
    )

    # 2. Change password & force the user to change it on next login
    api.mail_set_password_require_reset(mail, "TemporaryPassword456!")

    # 3. Upgrade or downgrade plan (e.g. 'light', 'standard', 'premium')
    api.mail_set_plan(mail, "premium")

    # 4. Set aliases and forwarders
    api.mail_set_aliases(mail, ["j.doe@example.com", "jane@example.com"])
    api.mail_set_forwards(mail, ["backup-inbox@example.com"])

    # 5. Increase storage quotas (in GB)
    api.mail_set_additional_mail_quota(mail, quota=10)
    api.mail_set_additional_cloud_quota(mail, quota=5)

    # 6. Configure Vacation / Out-of-Office autoresponder
    api.mail_vacation_set(
        mail=mail,
        subject="Out of Office",
        start_date="2026-07-01",
        end_date="2026-07-15",
        body="I am currently away and will reply upon my return."
    )

    # 7. Check vacation notice status
    vacation = api.mail_vacation_get(mail)

    # 8. Deactivate or re-activate an inbox
    api.mail_set_state(mail, active=False)  # Deactivate
    api.mail_set_state(mail, active=True)   # Re-activate

    # 9. Schedule future mailbox deletion (or delete immediately)
    api.mail_set_deletion_date(mail, deletion_date="2026-12-31")
    # api.mail_del(mail)
```

---

### 2. Managing Domains

Manage domains associated with your account, configure capabilities, and verify DNS records.

For all domain methods, see [Domain Methods in the Wiki](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#domain).

```python
with APIClient() as api:
    api.auth("admin@example.com", "YourPassword")

    account = "admin@example.com"
    domain = "mycompany.com"

    # List all domains for an account (returns names as a list)
    domain_names = api.domain_get_list(account)

    # Add a new domain
    api.domain_add(account=account, domain=domain, password="DomainPassword123!")

    # Configure domain capabilities
    # Options: MAIL_SPAMPROTECTION, MAIL_BLACKLIST, MAIL_BACKUPRECOVER, MAIL_PASSWORDRESET_SMS
    api.domain_capabilities_set(
        domain=domain,
        capabilities=["MAIL_SPAMPROTECTION", "MAIL_BLACKLIST"]
    )

    # Validate SPF DNS records for the domain
    spf_status = api.domain_validate_spf(domain)
    print(f"SPF validation result: {spf_status}")
```

---

### 3. Account Settings & Downloading Invoices

Retrieve account details, update company or payment information, and download billing invoices directly as PDF, CSV, or XML files.

For more information, see [Account Methods](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#account) and [Invoice Methods](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#invoice) in the Wiki.

```python
with APIClient() as api:
    api.auth("admin@example.com", "YourPassword")

    account = "admin@example.com"

    # Update account settings (e.g. payment method or contact details)
    api.account_set(account, payment_type="invoice", company="Acme Corp")

    # Get a list of all open invoice IDs
    open_invoices = api.account_invoice_get_list_open(account)
    print(f"Open invoices: {open_invoices}")

    # Download an invoice as a PDF file
    if open_invoices:
        invoice_id = open_invoices[0]
        
        # account_invoice_get_file automatically handles token retrieval,
        # Base64 decoding, and decompression, returning binary file bytes
        pdf_bytes = api.account_invoice_get_file(account, invoice_id, file_type="pdf")

        # Save to local file in binary mode ('wb')
        with open(f"{invoice_id}.pdf", "wb") as f:
            f.write(pdf_bytes)
        print(f"Saved invoice to {invoice_id}.pdf")
```

---

### 4. Object-Oriented Interface

If you prefer working with objects rather than raw dictionaries, the library provides dedicated object models: `Mail`, `Account`, and `Invoice`.

For full property tables and usage, see the [Object-Orientation Wiki](https://github.com/heshsum/mailbox-org-api/wiki/4.-Object-orientation).

```python
with APIClient() as api:
    api.auth("admin@example.com", "YourPassword")

    # Retrieve a Mail object
    user = api.mail_get_object("jane.doe@example.com")
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Plan: {user.plan}")
    print(f"Active: {user.active}")
    print(f"Aliases: {user.aliases}")

    # Retrieve an Account object
    acc = api.account_get_object("admin@example.com")
    print(f"Account: {acc.name}, Status: {acc.status}, Plan: {acc.plan}")

    # Retrieve an Invoice object
    invoices = api.account_invoice_get_list("admin@example.com")
    if invoices:
        inv = api.account_invoice_get_object("admin@example.com", invoices[0])
        print(f"Invoice {inv.invoice_id} dated {inv.date}, Status: {inv.status}")
```

---

### 5. Error Handling

API errors raise `APIError` with the corresponding error message and code returned by the mailbox.org Business API. Client-side input validation errors raise standard `ValueError` or `TypeError`.

```python
from mailbox_org_api.APIClient import APIClient
from mailbox_org_api.APIError import APIError

with APIClient() as api:
    api.auth("admin@example.com", "YourPassword")

    try:
        # Attempt an operation that might fail
        api.mail_get("nonexistent@example.com")
    except APIError as e:
        print(f"API request failed with code {e.code}: {e.message}")
    except (ValueError, TypeError) as e:
        print(f"Invalid parameter supplied: {e}")
```

---

## Wiki Documentation Reference

For in-depth guides and parameter reference tables, please visit the [Project Wiki](https://github.com/heshsum/mailbox-org-api/wiki):

| Topic | Wiki Page | Description |
| --- | --- | --- |
| **Installation** | [1. Installation](https://github.com/heshsum/mailbox-org-api/wiki/1.-Installation) | Package installation from PyPI and git source |
| **Getting Started** | [2. Basic Usage](https://github.com/heshsum/mailbox-org-api/wiki/2.-Basic-usage) | Client initialisation, debug mode, parameter validation, and response structures |
| **General Methods** | [3. Methods: General](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#general) | `auth`, `deauth`, `hello_world`, `hello_innerworld` |
| **Account Operations** | [3. Methods: Account](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#account) | Account retrieval, listing, setting attributes, and deletion |
| **Invoices** | [3. Methods: Invoice](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#invoice) | Listing invoices, tokens, and binary file downloads (`csv`, `pdf`, `xml`) |
| **Domain Management** | [3. Methods: Domain](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#domain) | Domain administration, SPF verification, capabilities configuration |
| **Mailbox Management** | [3. Methods: Mail](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#mail) | Mailbox CRUD, password reset, aliases, forwards, quotas, and backups |
| **Groups & Teams** | [3. Methods: Group](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#group) | Listing, creating, updating, and deleting group accounts |
| **Mailing Lists** | [3. Methods: Mailinglist](https://github.com/heshsum/mailbox-org-api/wiki/3.-Documentation-of-API-methods#mailinglist) | Managing mailing lists |
| **Object Models** | [4. Object Orientation](https://github.com/heshsum/mailbox-org-api/wiki/4.-Object-orientation) | Details on `Account`, `Invoice`, and `Mail` domain objects |

Official mailbox.org Business API documentation is available at [api.mailbox.org](https://api.mailbox.org).

---

## Contributing & License

Contributions, bug reports, and pull requests are welcome on [GitHub](https://github.com/heshsum/mailbox-org-api).

This project is licensed under the [MIT License](LICENSE).
