#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, FormView

from .forms import WalletForm, UpdateWalletForm, WebPaymentForm
from .models import Wallet


class ViewWallet(DetailView):
    model = Wallet


class UpdateWallet(UpdateView):
    form_class = UpdateWalletForm
    model = Wallet


class CreateWallet(CreateView):
    form_class = WalletForm
    model = Wallet
    success_url = reverse_lazy('view_wallet')


class MakeWebPayment(FormView):
    template_name = 'payline/web_payment.html'
    form_class = WebPaymentForm

    def form_valid(self, form):
        return HttpResponseRedirect(form.redirect_url)
