from unittest.mock import patch

import pytest

from mailbox_org_api.APIClient import APIClient


class TestAPIClientObjects:
    @pytest.mark.parametrize('attribute, value', [
        ('address_payment_same_as_main', False),
        ('av_contract_professional_secrecy', False),
        ('dta_allowed', False),
        ('old_customer', False),
        ('max_mailinglist', 0),
        ('monthly_fee', 0.0),
        ('company', ''),
        ('tarifflimits', []),
        ('contact', {}),
        ('company', 'Example'),
        ('dta_allowed', True),
    ])
    def test_account_get_object_preserves_values(self, attribute, value):
        api = APIClient()
        with patch.object(api, 'api_request', return_value={attribute: value}) as request:
            account = api.account_get_object('test_account')

        request.assert_called_once_with('account.get', {'account': 'test_account'})
        assert account.name == 'test_account'
        assert getattr(account, attribute) == value
        assert type(getattr(account, attribute)) is type(value)

    def test_account_get_object_skips_none(self):
        api = APIClient()
        result = {'name': None, 'contact': None, 'max_mailinglist': None}
        with patch.object(api, 'api_request', return_value=result):
            account = api.account_get_object('test_account')

        assert account.name == 'test_account'
        assert account.contact == {}
        assert not hasattr(account, 'max_mailinglist')
