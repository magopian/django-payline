from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'shop.views',
    url(r'^$', 'home', name='home'),
    url(r'^order/(?P<order_id>[\d]+)/', 'order_pay', name='order_pay'),
    url(r'^payment-success/$', 'payment_success', name='payment_success'),
    url(r'^payment-cancel/$', 'payment_cancel', name='payment_cancel'),
    url(r'^payment-notify/$', 'payment_notify', name='payment_notify'),
    url(r'^admin/', include(admin.site.urls)),
)
