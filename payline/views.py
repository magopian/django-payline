#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import WalletForm, UpdateWalletForm
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
