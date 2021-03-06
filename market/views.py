from django.http import Http404
from .models import PaymentSource, User, TraderTradesUsingCurrency, Transaction, DebitCard, Wallet
from django.shortcuts import render
from .context_processor import user_session_processor
import time

current_user = None
trade = None


# View function for home
def home(request):
    if 'current_user' not in request.session:
        set_user_session(request, empty=True)
    test = request.session['current_user']
    return render(request, 'market/home.html', {
        'error_message': "",
        'notification_message': "",
    })


def test(request):
    if 'current_user' not in request.session:
        set_user_session(request, True)
    user = request.session['current_user']
    return render(request, 'market/base.html', {'current_user': user})

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
    # TODO: create query - but for showing payment sources of ALL users
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
    global payment_source
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
    #  global payment_type
    #  global payment_source

    input_name = request.POST['name']
    input_type = request.POST['type']

    if input_name and input_type:
        # TODO: create query
      #  payment_type = input_type

        payment_source = PaymentSource()
        payment_source.name = input_name
        payment_source.u_id = current_user
        payment_source.created_on = str(get_datetime())
        payment_source.save()  # TODO: this will be replaced by a function call to query function

        if input_type == 'DebitCard':
            return render(request, 'market/debitcard_create.html', {
                'payment_source': payment_source,
            })

        else:
            return render(request, 'market/wallet_create.html', {
                'payment_source': payment_source,
            })
    else:
        return render(request, 'market/payment_source_new.html', {
            'error_message': "Please fill out all the fields."
        })


def payment_source_new(request):
    not_signed_in_check(request)
    return render(request, 'market/payment_source_new.html')

# def payment_source_edit(request):
#     not_signed_in_check(request)
#     if payment_type == 'DebitCard':
#         return render(request, 'market/debitcard_edit.html')
#     else:
#         return render(request, 'market/wallet_edit.html')

# def debitcard_detail(request, dc_id):
#     not_signed_in_check(request)
#     debit = DebitCard.objects.get(pk=dc_id)
#     return render(request, 'market/payment_source_detail.html', {'DebitCard': debit})


def debitcard_create(request, payment_source):
    not_signed_in_check(request)

    input_bank_name = request.POST.get('bank_name', None)
    input_card_number = request.POST.get('cnumber', None)
    input_name = request.POST.get('name', None)
    input_expiry_date = request.POST.get('expirydate', None)

    if input_bank_name and input_card_number and input_name and input_expiry_date:
        debit = DebitCard()
        debit.card_pmnt_src_id = payment_source
        debit.bank_name = input_bank_name
        debit.name = input_name
        debit.card_number = input_card_number
        debit.expiry_date = input_expiry_date
        debit.save()

        return render(request, 'market/payment_source_detail.html', {
            'paymnt_source': payment_source,
            'debit': debit,
        })
    else:
        return render(request, 'market/debitcard_create.html', {
            'error_message': "Please fill out all the fields."
        })


def wallet_create(request, payment_source):
    not_signed_in_check(request)

    input_max_limit = request.POST.get('max_limit', None)

    if input_max_limit:
        wallet = Wallet()
        wallet.wallet_pmnt_src_id = payment_source
        wallet.max_limit = input_max_limit
        wallet.save()

        return render(request, 'market/payment_source_detail.html', {
            'paymnt_source': payment_source,
            'wallet': wallet,
        })
    else:
        return render(request, 'market/wallet_create.html', {
            'error_message': "Please fill out all the fields."
        })


# *********************************************** Transaction

'''
    transaction_new_select_source > transaction_new & create_trader_trades_using_currency
        > transaction_create
    new transaction query sequence:
    payment_source > payment_source_id > PaymentSourceHasCurrency > currency_name
    using the currency_name, a new TraderTradesUsingCurrency object will be created.
    (trader_id=current_user_id)
'''


def transaction_new_select_source(request):
    # asks user which payment source they want to use to create the transaction.
    not_signed_in_check(request)
    user_all_ps = PaymentSource.objects.filter(u_id=current_user.user_id)
    return render(request, 'market/transaction_new_select_source.html', {
        'all_payment_sources': user_all_ps,
    })


def transaction_new(request, payment_source_id):
    # creates a new TraderTradesUsingCurrency object
    # with currency name acquired from payment_source_id
    # renders new form at end
    global trade
    not_signed_in_check(request)
    trade = create_trader_trades_using_currency(payment_source_id)
    return render(request, 'market/transaction_new.html')


def transaction_create(request):
    input_amount = request.POST['amount']
    if input_amount:
        transaction = Transaction()
        transaction.amount = input_amount
        transaction.date = str(get_datetime())
        # transaction.save
        return render(request, 'market/transaction_detail.html', {
            'transaction': transaction,
        })
    else:
        return render(request, 'market/transaction_new.html', {
            'error_message': "Please fill out all the fields."
        })


def transaction_detail(request, transaction_id):
    not_signed_in_check(request)
    # TODO:
    '''
    PaymentSource.objects.get(pk=ps_id)
        Given a transaction_id, get the corresponding transaction.
    '''
    transaction = ''  # TODO: create query
    return render(request, 'market/transaction_detail.html', {'transaction': transaction})


def create_trader_trades_using_currency(payment_source_id):
    # get payment_source's currency name
    new_trade = TraderTradesUsingCurrency()
    cur_name = ''  # TODO: query goes here.
    # get paymentsource's currency using given payment_source_id
    new_trade.trader_id = current_user.user_id
    new_trade.currency_name = cur_name
    return new_trade


def all_transactions(request):
    not_signed_in_check(request)
    all_trs = PaymentSource.objects.all()
    # TODO: create query - for showing transactions for ALL users (admin functionality)
    context = {'all_transactions': all_trs}
    return render(request, 'market/transaction_all.html', context)


def all_user_transactions(request, user_id):
    not_signed_in_check(request)
    user_all_trs = Transaction.objects.filter(trader_id=user_id)
    # TODO:
    '''
    PaymentSource.objects.filter(u_id=user_id)
        Given a foreign key user_id, get all the corresponding transactions.
        (get all the payment sources of a given user)
    '''
    return render(request, 'market/transaction_all.html', {
        'all_transaction': user_all_trs,
    })


# ********************************************* Relationships


# returns today's date and time
def get_datetime():
    datetime = time.strftime("%Y-%m-%d %H:%M")
    return datetime
