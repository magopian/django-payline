#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from logging import getLogger
from os import path
from uuid import uuid4

from django.conf import settings
from django.utils.translation import ugettext as _
from suds import WebFault
from suds.client import Client


logger = getLogger('payline')


class PaylineProcessor(object):
    """Payline Payment Backend."""

    AUTHORIZE = 100
    AUTHORIZE_AND_VALIDATE = 101

    PAYMENT_SUCCESS = "00000"

    def __init__(self):
        """Instantiate suds client."""
        wsdl_dir = path.join(path.abspath(path.dirname(__file__)), 'wsdl/v4_0')

        payline_api = getattr(settings, 'PAYLINE_API', 'DirectPayment')
        if payline_api not in ('DirectPayment', 'WebPayment', 'MassPayment'):
            raise ValueError("Unsupported Payline API: %s" % payline_api)

        debug_mode = getattr(settings, 'PAYLINE_DEBUG', True)
        environment = 'homologation' if debug_mode else 'production'
        wsdl_path = path.join(wsdl_dir, environment, "%sAPI.wsdl" % payline_api)
        wsdl_uri = 'file://%s' % wsdl_path

        merchant_id = getattr(settings, 'PAYLINE_MERCHANT_ID', '')
        api_key = getattr(settings, 'PAYLINE_KEY', '')
        self.vad_number = getattr(settings, 'PAYLINE_VADNBR', '')
        # Fallback to Euro if no currency code is defined in the settings.
        self.currency_code = getattr(settings, 'PAYLINE_CURRENCY_CODE', 978)
        self.client = Client(url=wsdl_uri,
                             username=merchant_id,
                             password=api_key)

    def validate_card(self, card_number, card_type, card_expiry, card_cvx):
        """Do an Authorization request to make sure the card is valid."""
        minimum_amount = 100  # 1€ is the smallest amount authorized
        payment = self.client.factory.create('ns1:payment')
        payment.amount = minimum_amount
        payment.currency = self.currency_code
        payment.action = self.AUTHORIZE
        payment.mode = 'CPT'  # CPT = comptant
        payment.contractNumber = self.vad_number
        order = self.client.factory.create('ns1:order')
        order.ref = str(uuid4())
        order.amount = minimum_amount
        order.currency = self.currency_code
        order.date = datetime.now().strftime("%d/%m/%Y %H:%M")
        card = self.client.factory.create('ns1:card')
        card.number = card_number
        card.type = card_type
        card.expirationDate = card_expiry
        card.cvx = card_cvx
        try:
            res = self.client.service.doAuthorization(payment=payment,
                                                      order=order,
                                                      card=card)
        except WebFault:
            logger.error("Payment backend failure", exc_info=True)
            return (False, None,
                    _("Payment backend failure, please try again later."))
        result = (res.result.code == self.PAYMENT_SUCCESS,
                  res.result.shortMessage + ': ' + res.result.longMessage)
        if result[0]:  # authorization was successful, now cancel it (clean up)
            self.client.service.doReset(transactionID=res.transaction.id,
                                        comment='Card validation cleanup')
        return result

    def create_update_wallet(self, wallet_id, last_name, first_name,
                             card_number, card_type, card_expiry, card_cvx,
                             create=True):
        """Create or update a customer wallet to hold payment information.

        Return True if the creation or update was successful.

        """
        wallet = self.client.factory.create('ns1:wallet')
        wallet.walletId = wallet_id
        wallet.lastName = last_name
        wallet.firstName = first_name
        wallet.card = self.client.factory.create('ns1:card')
        wallet.card.number = card_number
        wallet.card.type = card_type
        wallet.card.expirationDate = card_expiry
        wallet.card.cvx = card_cvx
        service = self.client.service.createWallet
        if not create:
            service = self.client.service.updateWallet
        try:
            res = service(contractNumber=self.vad_number, wallet=wallet)
        except:
            logger.error("Payment backend failure", exc_info=True)
            return (False,
                    _("Payment backend failure, please try again later."))
        return (res.result.code == "02500",  # success ?
                res.result.shortMessage + ': ' + res.result.longMessage)

    def get_wallet(self, wallet_id):
        """Get wallet information from Payline."""
        try:
            res = self.client.service.getWallet(
                contractNumber=self.vad_number,
                walletId=wallet_id)
        except WebFault:
            logger.error("Payment backend failure", exc_info=True)
            return (False,
                    _("Payment backend failure, please try again later."))
        return (res.result.code == "02500",  # success ?
                getattr(res, 'wallet', None),  # None is needed because of suds
                res.result.shortMessage + ': ' + res.result.longMessage)

    def make_wallet_payment(self, wallet_id, amount):
        """Make a payment from the given wallet."""
        amount_cents = amount * 100  # use the smallest unit possible (cents)
        payment = self.client.factory.create('ns1:payment')
        payment.amount = amount_cents
        payment.currency = self.currency_code
        payment.action = self.AUTHORIZE_AND_VALIDATE
        payment.mode = 'CPT'  # CPT = comptant
        payment.contractNumber = self.vad_number
        order = self.client.factory.create('ns1:order')
        order.ref = str(uuid4())
        order.amount = amount_cents
        order.currency = self.currency_code
        order.date = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            res = self.client.service.doImmediateWalletPayment(
                payment=payment,
                order=order,
                walletId=wallet_id)
        except WebFault:
            logger.error("Payment backend failure", exc_info=True)
            return (False, None,
                    _("Payment backend failure, please try again later."))
        return (res.result.code == self.PAYMENT_SUCCESS,
                res.transaction.id,
                res.result.shortMessage + ': ' + res.result.longMessage)

    def make_web_payment(self, order_ref, amount):
        amount_cents = int(float(amount) * 100)
        payment = self.client.factory.create('ns1:payment')
        payment.amount = amount_cents
        payment.currency = self.currency_code
        payment.action = self.AUTHORIZE_AND_VALIDATE
        payment.mode = 'CPT'
        payment.contractNumber = self.vad_number

        order = self.client.factory.create('ns1:order')
        order.ref = order_ref
        order.amount = amount_cents
        order.currency = self.currency_code
        order.date = datetime.now().strftime("%d/%m/%Y %H:%M")

        return_url = getattr(settings, 'PAYLINE_RETURN_URL', '')
        cancel_url = getattr(settings, 'PAYLINE_CANCEL_URL', '')
        notification_url = getattr(settings, 'PAYLINE_NOTIFICATION_URL', '')

        try:
            res = self.client.service.doWebPayment(
                payment=payment,
                returnURL=return_url,
                cancelURL=cancel_url,
                order=order,
                notificationURL=notification_url,
                selectedContractList=(self.vad_number, )
            )
        except WebFault:
            logger.error("Payment backend failure", exc_info=True)
            return (False, None,
                    _("Payment backend failure, please try again later."))
        return (res.result.code == self.PAYMENT_SUCCESS,
                res.redirectURL,
                res.result.shortMessage + ': ' + res.result.longMessage)
