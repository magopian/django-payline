#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import time

from django import forms
from django.conf import settings
from django.utils import unittest
from mock import patch

from .forms import (expiry_date_to_datetime, validate_expiry_date,
                    obfuscate_card_number, WalletForm, UpdateWalletForm,
                    WalletCreationError)
from .models import Wallet, Transaction
from .processor import PaylineProcessor


EXPIRY = datetime.now() + timedelta(days=365)  # somewhere in the future

PAYLINE_TEST_CARD_TYPE = "CB"
PAYLINE_TEST_CARD_NUMBER = "4970100000325734"
PAYLINE_TEST_CARD_EXPIRY = EXPIRY.strftime("%m%y")
PAYLINE_TEST_CARD_CVX = "123"


@unittest.skipUnless(getattr(settings, 'PAYLINE_KEY', False),
                     "No settings.PAYLINE_KEY set")
class PaylineProcessorTest(unittest.TestCase):
    """Integration test with Payline."""
    wallet_id = 'test_%s' % time()  # one wallet id for all the test cases
    pp = PaylineProcessor()
    wallet_data = {'wallet_id': wallet_id,
                   'last_name': 'Potter',
                   'first_name': 'Harry',
                   'card_number': PAYLINE_TEST_CARD_NUMBER,
                   'card_type': PAYLINE_TEST_CARD_TYPE,
                   'card_expiry': PAYLINE_TEST_CARD_EXPIRY,
                   'card_cvx': PAYLINE_TEST_CARD_CVX}

    def _test_create_wallet_bad_card(self):
        bad_wallet_data = self.wallet_data.copy()
        bad_wallet_data['card_number'] = '1234'
        result, message = self.pp.create_update_wallet(**bad_wallet_data)
        self.assertFalse(result, message)

    def _test_create_wallet(self):
        result, message = self.pp.create_update_wallet(**self.wallet_data)
        self.assertTrue(result, message)

    def _test_get_wallet(self):
        result, wallet, message = self.pp.get_wallet('foobar')
        self.assertFalse(result)
        result, wallet, message = self.pp.get_wallet(self.wallet_id)
        self.assertTrue(result)
        self.assertEqual(wallet.walletId, self.wallet_id)

    def _test_update_wallet_bad_card(self):
        bad_wallet_data = self.wallet_data.copy()
        bad_wallet_data['card_number'] = '1234'
        result, message = self.pp.create_update_wallet(create=False,
                                                       **bad_wallet_data)
        self.assertFalse(result, message)

    def _test_update_wallet(self):
        result, message = self.pp.create_update_wallet(create=False,
                                                       **self.wallet_data)
        self.assertTrue(result, message)

    def _test_make_wallet_payment(self):
        result, transaction_id, message = self.pp.make_wallet_payment(
            wallet_id=self.wallet_data['wallet_id'],
            amount=1)
        self.assertTrue(result, message)
        self.assertIsNotNone(transaction_id)

    def test_payline_integration(self):
        """Payline processor integration tests."""
        # run tests in order to have wallet created before being updated
        self._test_create_wallet_bad_card()
        self._test_create_wallet()
        self._test_get_wallet()
        self._test_update_wallet_bad_card()
        self._test_update_wallet()
        self._test_make_wallet_payment()

    def test_validate_card_bad_number(self):
        card_data = {'card_number': '1234',
                     'card_type': PAYLINE_TEST_CARD_TYPE,
                     'card_expiry': PAYLINE_TEST_CARD_EXPIRY,
                     'card_cvx': PAYLINE_TEST_CARD_CVX}
        result, message = self.pp.validate_card(**card_data)
        self.assertFalse(result, message)

    def test_validate_card(self):
        card_data = {'card_number': PAYLINE_TEST_CARD_NUMBER,
                     'card_type': PAYLINE_TEST_CARD_TYPE,
                     'card_expiry': PAYLINE_TEST_CARD_EXPIRY,
                     'card_cvx': PAYLINE_TEST_CARD_CVX}
        result, message = self.pp.validate_card(**card_data)
        self.assertTrue(result, message)


class WalletFormTest(unittest.TestCase):

    def test_validate_expiry_date(self):
        with self.assertRaisesRegexp(forms.ValidationError,
                                     "Expiry date format must be MMYY"):
            validate_expiry_date('1312')  # bad format
        with self.assertRaisesRegexp(forms.ValidationError,
                                     "Expiry date must be in the future"):
            validate_expiry_date('1200')  # past expiry

    def test_obfuscate_card_number(self):
        # normal
        obfuscated = obfuscate_card_number('4970100000325734')
        self.assertEqual(obfuscated, 'XXXXXXXXXXXX5734')
        # short
        obfuscated = obfuscate_card_number('5734')
        self.assertEqual(obfuscated, '5734')
        # very short
        obfuscated = obfuscate_card_number('')
        self.assertEqual(obfuscated, '')

    def test_save(self):
        form = WalletForm({'last_name': 'Potter',
                           'first_name': 'Harry',
                           'card_number': PAYLINE_TEST_CARD_NUMBER,
                           'card_type': PAYLINE_TEST_CARD_TYPE,
                           'card_expiry': PAYLINE_TEST_CARD_EXPIRY,
                           'card_cvx': PAYLINE_TEST_CARD_CVX})

        def fake_ok(*args, **kwargs):
            return True, 'OK'

        def fake_nok(*args, **kwargs):
            return False, 'Not OK'

        with patch.object(PaylineProcessor, 'validate_card', fake_ok):
            form.is_valid()

        with self.assertRaisesRegexp(WalletCreationError, 'Not OK'):
            with patch.object(PaylineProcessor, 'create_update_wallet',
                              fake_nok):
                form.save(commit=False)


@unittest.skipUnless(getattr(settings, 'PAYLINE_KEY', False),
                     "No settings.PAYLINE_KEY set")
class WalletFormIntegrationTest(unittest.TestCase):
    """Form tests and integration test with Payline."""

    def setUp(self):
        self.pp = PaylineProcessor()
        self.wallet_data = {'last_name': 'Potter',
                            'first_name': 'Harry',
                            'card_number': PAYLINE_TEST_CARD_NUMBER,
                            'card_type': PAYLINE_TEST_CARD_TYPE,
                            'card_expiry': PAYLINE_TEST_CARD_EXPIRY,
                            'card_cvx': PAYLINE_TEST_CARD_CVX}

    def _check_local_payline_wallet(self, wallet):
        result, payline_wallet, message = self.pp.get_wallet(wallet.wallet_id)
        self.assertTrue(result)
        self.assertEqual(wallet.first_name, payline_wallet.firstName)
        self.assertEqual(wallet.last_name, payline_wallet.lastName)
        self.assertEqual(wallet.card_number[-4:],
                         payline_wallet.card.number[-4:])
        self.assertEqual(wallet.card_expiry,
                         payline_wallet.card.expirationDate)
        self.assertEqual(wallet.card_type, payline_wallet.card.type)

    def _test_wallet_form_good_card_empty_name(self):
        bad_wallet_data = self.wallet_data.copy()
        bad_wallet_data['first_name'] = ''
        form = WalletForm(bad_wallet_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(Wallet.objects.count(), 0)

    def _test_wallet_form_bad_card(self):
        bad_wallet_data = self.wallet_data.copy()
        bad_wallet_data['card_number'] = '1234'
        form = WalletForm(bad_wallet_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(Wallet.objects.count(), 0)

    def _test_wallet_form(self):
        form = WalletForm(self.wallet_data)
        self.assertTrue(form.is_valid(), form.errors)
        wallet = form.save()
        self.assertEqual(wallet.first_name, 'Harry')
        self.assertEqual(wallet.last_name, 'Potter')
        obfuscated = obfuscate_card_number(PAYLINE_TEST_CARD_NUMBER)
        self.assertEqual(wallet.card_number, obfuscated)
        self.assertEqual(wallet.card_type, PAYLINE_TEST_CARD_TYPE)
        self.assertEqual(wallet.card_expiry, PAYLINE_TEST_CARD_EXPIRY)
        self._check_local_payline_wallet(wallet)
        self.assertEqual(Wallet.objects.count(), 1)

    def _test_update_wallet_form_good_card_empty_name(self):
        wallet = Wallet.objects.all()[0]
        bad_wallet_data = self.wallet_data.copy()
        bad_wallet_data['first_name'] = ''
        form = UpdateWalletForm(bad_wallet_data, instance=wallet)
        self.assertFalse(form.is_valid())
        self.assertEqual(Wallet.objects.count(), 1)

    def _test_update_wallet_form_bad_card(self):
        wallet = Wallet.objects.all()[0]
        bad_wallet_data = self.wallet_data.copy()
        bad_wallet_data['card_number'] = '1234'
        form = UpdateWalletForm(bad_wallet_data, instance=wallet)
        self.assertFalse(form.is_valid())
        self.assertEqual(Wallet.objects.count(), 1)

    def _test_update_wallet_form(self):
        wallet = Wallet.objects.all()[0]
        self.wallet_data['first_name'] = 'Johnny'
        form = UpdateWalletForm(self.wallet_data, instance=wallet)
        self.assertTrue(form.is_valid())
        wallet = form.save()
        self._check_local_payline_wallet(wallet)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(wallet.first_name, 'Johnny')

    def test_form_integration(self):
        """Form integration tests."""
        # run tests in order to have wallet created before being updated
        self._test_wallet_form_good_card_empty_name()
        self._test_wallet_form_bad_card()
        self._test_wallet_form()
        self._test_update_wallet_form_good_card_empty_name()
        self._test_update_wallet_form_bad_card()
        self._test_update_wallet_form()


class WalletModelTest(unittest.TestCase):

    def setUp(self):
        self.wallet_data = {'last_name': 'Potter',
                            'first_name': 'Harry',
                            'card_number': PAYLINE_TEST_CARD_NUMBER,
                            'card_type': PAYLINE_TEST_CARD_TYPE}

    def test_expiry_date_to_datetime(self):
        self.assertEqual(expiry_date_to_datetime('1212'),  # end of year
                         datetime(2012, 12, 31))
        self.assertEqual(expiry_date_to_datetime('0112'),  # beginning of year
                         datetime(2012, 01, 31))
        self.assertEqual(expiry_date_to_datetime('0212'),  # leap year
                         datetime(2012, 02, 29))
        self.assertEqual(expiry_date_to_datetime('0213'),
                         datetime(2013, 02, 28))

    def test_is_valid_future(self):
        wallet = Wallet(**self.wallet_data)
        wallet.card_expiry = (datetime.today() +
                              timedelta(days=32)).strftime('%m%y')
        self.assertTrue(wallet.is_valid())

    def test_is_valid_current_month(self):
        wallet = Wallet(**self.wallet_data)
        wallet.card_expiry = datetime.today().strftime('%m%y')
        self.assertTrue(wallet.is_valid())

    def test_is_valid_past(self):
        wallet = Wallet(**self.wallet_data)
        wallet.card_expiry = (datetime.today() -
                              timedelta(days=32)).strftime('%m%y')
        self.assertFalse(wallet.is_valid())

    def test_expires_this_month(self):
        wallet = Wallet(**self.wallet_data)
        wallet.card_expiry = datetime.today().strftime('%m%y')
        self.assertTrue(wallet.expires_this_month())

    def test_expires_this_month_next_year(self):
        wallet = Wallet(**self.wallet_data)
        today = datetime.today()
        next_year = datetime(year=today.year + 1, month=today.month, day=1)
        wallet.card_expiry = next_year.strftime('%m%y')
        self.assertFalse(wallet.expires_this_month())

    def test_expires_this_month_past(self):
        wallet = Wallet(**self.wallet_data)
        wallet.card_expiry = (datetime.today() -
                              timedelta(days=32)).strftime('%m%y')
        self.assertFalse(wallet.expires_this_month())

    def test_make_payment(self):
        num_transactions = Transaction.objects.count()
        wallet = Wallet(**self.wallet_data)
        with patch.object(PaylineProcessor, 'make_wallet_payment',
                          lambda s, wid, amount: [True, 'foo', 'ok']):
            result, message = wallet.make_payment(123)
        self.assertTrue(result, message)
        self.assertEqual(Transaction.objects.count(), num_transactions + 1)

    def test_make_payment_refused(self):
        num_transactions = Transaction.objects.count()
        wallet = Wallet(**self.wallet_data)
        with patch.object(PaylineProcessor, 'make_wallet_payment',
                          lambda s, wid, amount: [False, None, 'ko']):
            result, message = wallet.make_payment(123)
        self.assertFalse(result)
        self.assertEqual(Transaction.objects.count(), num_transactions)
