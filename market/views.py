from django.http import Http404
from .models import PaymentSource
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<h1>This is the market homepage.</h1>")


def payment_sources(request):
    all_payment_sources = PaymentSource.objects.all() # TODO: create query
    context = {'all_payment_sources': all_payment_sources}
    return render(request, 'market/payment_sources.html', context)


def payment_source_detail(request, payment_source_id):
    try:
        payment_source = PaymentSource.objects.get(pk=payment_source_id) # TODO: create query
    except PaymentSource.DoesNotExist:
        raise Http404("Payment Source does not exist.")
    return render(request, 'market/payment_source_detail.html', {'payment_source': payment_source})
