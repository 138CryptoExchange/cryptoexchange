from django.http import Http404
from .models import PaymentSource, User
from django.shortcuts import render
from .context_processor import user_session_processor
import time

current_user = None


# View function for home
def home(request):
    if 'current_user' not in request.session:
        set_user_session(request, empty=True)
    test = request.session['current_user']
    return render(request, 'market/home.html', {
        'error_message': "",
        'notification_message': "",
    })


# ********************************************* User

def get_current_user(new=False, current_user_id=None):
    global current_user
    if not new and current_user:
        return current_user
    elif new and current_user_id is not None:
        current_user_object = User.objects.get(pk=current_user_id)
        current_user = current_user_object
        current_user_tuple = get_user_tuple(current_user_object)
        return current_user_tuple
    else:
        return False


def get_user_tuple(current_user_object):
    current_user_tuple = {
        'user_id': current_user_object.user_id,
        'name': current_user_object.name,
        'email': current_user_object.email,
        'address': current_user_object.address,
        'pnumber': current_user_object.phone_number,
        'type': current_user_object.user_type
    }
    return current_user_tuple


def not_signed_in_check(request):
    global current_user
    if 'current_user' not in request.session or \
            request.session['current_user'] is None or \
            current_user is None:
        set_user_session(request, empty=True)
        return render(request, 'market/user_signup.html', {
            'error_message': "You must be signed in to view that page.",
        })
    else:
        return None


def signed_in_check(request):
    global current_user
    if 'current_user' in request.session and \
            request.session['current_user'] is not None \
            and current_user is not None:
        return render(request, 'market/user_profile.html', {
            'user_id': request.session['current_user'].user_id,
            'error_message': "You are already signed in.",
        })
    else:
        return None


def set_user_session(request, user_id=None, empty=False):
    global current_user
    if not empty and user_id:
        request.session['current_user'] = get_current_user(True, user_id)
        user_session_processor(request)
    else:
        request.session['current_user'] = None
        current_user = None
        user_session_processor(request)


def user_signin(request):
    not_signed_in_check(request)
    set_user_session(request, empty=True)
    return render(request, 'market/user_signin.html')


def user_signin_redirect(request):
    input_name = request.POST['name']
    input_email = request.POST['email']
    #TODO:
    '''
    User.objects.get(name=input_name, email=input_email)
        Query that checks whether the User table has a row with the given 'name'
        and 'email' attributes. If it does exist, return the user object. If it 
        doesn't exist, return None. 
    User.objects.filter(name=input_name, email=input_email).exists()
        Query that checks whether the User table has a row with the given 'name'
        and 'email' attributes, and returns a boolean accordingly. This is necessary
        to check whether the object exists or not before performing a query. Thats why
        this one is being used in the if condition.
    '''
    if input_email and input_name and User.objects.filter(name=input_name, email=input_email).exists():
        user = User.objects.get(name=input_name, email=input_email)
        set_user_session(request, user.user_id)
        return render(request, 'market/user_profile.html', {
            'user_id': user.user_id,
            'notification_message': 'Signed In Successfully',
        })
    else:
        return render(request, 'market/user_signin.html', {
            'error_message': "Incorrect or invalid inputs."
        })


def user_signout(request):
    not_signed_in_check(request)
    set_user_session(request, empty=True)
    return render(request, 'market/home.html', {
        'notification_message': 'Signed out successfully.',
    })


def user_signup(request):
    signed_in_check(request)
    set_user_session(request, empty=True)
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
        set_user_session(request, user.user_id)
        return render(request, 'market/user_profile.html', {
            'user_id': user.user_id,
            'notification_message': 'Account created successfully',
        })
    else:
        return render(request, 'market/user_signup.html', {
            'error_message': "Required Fields: Name, Email, and Account Type."
        })


def user_profile(request, user_id):
    check = not_signed_in_check(request)
    if check is not None:
        return check
    global current_user
    try:
        if user_id == current_user.user_id:
            user = current_user
        else:
            user = User.objects.get(pk=user_id)  # TODO: create query
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    return render(request, 'market/user_profile.html', {'user': user})


# ********************************************* Payment Source

def all_payment_sources(request):
    not_signed_in_check(request)
    all_ps = PaymentSource.objects.all()
    # TODO: create query - but only for showing payment sources of ALL users
    context = {'all_payment_sources': all_ps}
    return render(request, 'market/all_payment_sources.html', context)


def all_user_payment_sources(request, user_id):
    not_signed_in_check(request)
    user_all_ps = PaymentSource.objects.filter(u_id=user_id)
    # TODO:
    '''
    PaymentSource.objects.filter(u_id=user_id)
        Given a foreign key user_id, get all the corresponding payment sources.
        (get all the payment sources of a given user)
    '''
    return render(request, 'market/all_payment_sources.html', {
        'all_payment_sources': user_all_ps,
    })


def payment_source_detail(request, ps_id):
    not_signed_in_check(request)
    # TODO:
    '''
    PaymentSource.objects.get(pk=ps_id)
        Given a payment_source_id, get the corresponding payment source.
    '''
    payment_source = PaymentSource.objects.get(pk=ps_id) # TODO: create query
    return render(request, 'market/payment_source_detail.html', {'paymnt_src': payment_source})


def payment_source_create(request):
    not_signed_in_check(request)
    global current_user
    input_name = request.POST['name']
    if input_name:
        # TODO: create query
        payment_source = PaymentSource()
        payment_source.name = input_name
        payment_source.u_id = current_user
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


# ********************************************* Relationships


# returns today's date and time
def get_datetime():
    datetime = time.strftime("%Y-%m-%d %H:%M")
    return datetime
