from django.http import Http404
from .models import PaymentSource, User
from django.http import HttpResponse
from django.shortcuts import render
import time

user_signed_in = False


def home(request):
    if 'current_user' not in request.session:
        request.session['current_user'] = None
        request.session['user_type'] = None
    return render(request, 'market/home.html')


# ********************************************* User

def not_signed_in_check(request):
    if 'current_user' not in request.sesuser_checksion or not request.session['current_user']:
        return render(request, 'market/user_signup.html', {
            'error_message': "You must be signed in to view that page.",
        })


def signed_in_check(request):
    if 'current_user' in request.session and request.session['current_user'] is not none:
        return render(request, 'market/user_profile.html', {
            'user_id': request.session['current_user'],
            'error_message': "You are already signed in.",
        })


def user_signup(request):
    request.session['current_user'] = None
    request.session['user_type'] = None
    return render(request, 'market/user_signup.html')


def user_create(request):
    input_email = request.POST['email']
    input_pnumber = request.POST['pnumber']
    input_name = request.POST['name']
    input_address = request.POST['address']
    input_type = request.POST['type']

    if input_email and input_name and input_type:
        # TODO: create query
        user = User()
        user.email = input_email
        user.phone_number = input_pnumber
        user.name = input_name
        user.address = input_address
        user.user_type = input_type
        user.save()
        request.session['current_user'] = user
        request.session['user_type'] = user.user_type
        return render(request, 'market/user_profile.html', {
            'user_id': user.user_id,
        })
    else:
        return render(request, 'market/user_signup.html', {
            'error_message': "Required Fields: Name, Email, and Account Type."
        })


def user_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id) # TODO: create query
    except User.DoesNotExist:
        raise Http404("User Source does not exist.")
    return render(request, 'market/user_profile.html', {'user': user})


# ********************************************* Payment Source

def all_payment_sources(request):
    not_signed_in_check(request)
    all_ps = PaymentSource.objects.all() # TODO: create query
    context = {'all_payment_sources': all_ps}
    return render(request, 'market/all_payment_sources.html', context)


def payment_source_detail(request, payment_source_id):
    not_signed_in_check(request)
    try:
        payment_source = PaymentSource.objects.get(pk=payment_source_id) # TODO: create query
    except PaymentSource.DoesNotExist:
        raise Http404("Payment Source does not exist.")
    return render(request, 'market/payment_source_detail.html', {'payment_source': payment_source})


def payment_source_create(request):
    not_signed_in_check(request)
    input_name = request.POST['name']
    if input_name:
        # TODO: create query
        payment_source = PaymentSource()
        payment_source.name = input_name
        payment_source.u_id = request.session['current_user'] # TODO: create current user
        payment_source.created_on = str(get_datetime())
        payment_source.save()  # TODO: this will be replaced by a function call to query function
        return render(request, 'market/payment_source_detail.html', {
            'payment_source': payment_source
        })
    else:
        return render(request, 'market/payment_source_new.html', {
            'error_message': "Please fill out all the fields."
        })


def payment_source_new(request):
    not_signed_in_check(request)
    return render(request, 'market/payment_source_new.html')


# returns today's date and time
def get_datetime():
    datetime = time.strftime("%Y-%m-%d %H:%M")
    return datetime
