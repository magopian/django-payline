from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from payline.processor import PaylineProcessor
from payline.forms import WebPaymentForm


def home(request):
    if request.method == 'POST':
        order = models.Order(
            amount=100.00
        )
        order.save()
        return redirect('order_pay', order_id=order.id)
    return render(request, 'home.html')


def order_pay(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    form = WebPaymentForm(request.POST,
                          order_ref=order.identifier,
                          amount=order.amount)
    if request.method == 'POST' and form.is_valid():
        transaction = form.save()
        transaction.order_object = order
        transaction.save()
        return redirect(form.redirect_url)
    return render(request, 'order_pay.html', {'form': form})


def payment_success(request):
    return render(request, 'payment_success.html')


def payment_cancel(request):
    return render(request, 'payment_cancel.html')


def payment_notify(request):
    token = request.GET.get('token')
    if not token:
        raise Http404
    pp = PaylineProcessor()
    success, payment_details = pp.get_web_payment_details(token)
