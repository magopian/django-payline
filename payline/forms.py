#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Wallet, get_uuid4, expiry_date_to_datetime
from .processor import PaylineProcessor


def validate_expiry_date(expiry_date):
    """Validate that the expiry date is valid."""
    try:
        exp = expiry_date_to_datetime(expiry_date)
    except ValueError:
        raise forms.ValidationError(_("Expiry date format must be MMYY"))
    if exp < datetime.today():
        raise forms.ValidationError(_("Expiry date must be in the future"))
    return exp


def obfuscate_card_number(card_number):
    """Obfuscate everything but the last four chars from a card number."""
    length = len(card_number)
    obfuscated = 'X' * (length - 4)
    return obfuscated + card_number[-4:]


class WalletForm(forms.ModelForm):
    """Create or update a wallet."""
    card_cvx = forms.CharField(label=_('Card CVX code'),
                               help_text=_('Security code, three numbers from '
                                           'the back of the payment card'),
                               max_length=3)

    class Meta:
        model = Wallet

    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)
        self.pp = PaylineProcessor()
        self.create = True
        self.wallet_id = get_uuid4()

    def clean_card_expiry(self):
        expiry_date = self.cleaned_data['card_expiry']
        validate_expiry_date(expiry_date)
        return expiry_date

    def clean(self):
        """Validate that the card is correct by creating a Payline wallet."""
        cleaned_data = super(WalletForm, self).clean()
        # do not attempt a creation or update of wallet unless form is valid
        if self.errors:
            return cleaned_data
        result, message = self.pp.create_update_wallet(
            wallet_id=self.wallet_id,
            last_name=cleaned_data.get('last_name'),
            first_name=cleaned_data.get('first_name'),
            card_number=cleaned_data.get('card_number'),
            card_type=cleaned_data.get('card_type'),
            card_expiry=cleaned_data.get('card_expiry'),
            card_cvx=cleaned_data.get('card_cvx'),
            create=self.create)
        if not result:
            raise forms.ValidationError(message)
        return cleaned_data

    def save(self, commit=True):
        """Create wallet on Payline."""
        wallet = super(WalletForm, self).save(commit=commit)
        wallet.wallet_id = self.wallet_id
        wallet.card_number = obfuscate_card_number(wallet.card_number)
        if commit:
            wallet.save()
        return wallet


class UpdateWalletForm(WalletForm):

    def __init__(self, *args, **kwargs):
        super(UpdateWalletForm, self).__init__(*args, **kwargs)
        self.create = False
        self.wallet_id = self.instance.wallet_id
        self.initial['card_number'] = ''
        self.initial['card_type'] = None
        self.initial['card_expiry'] = ''
        self.initial['card_cvx'] = ''
