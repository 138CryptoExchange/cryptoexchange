from django.urls import path
from . import views


urlpatterns = [
    # /market/
    path('', views.home, name='home'),

    # /sign_up
    path('sign_up', views.user_signup, name='user_signup'),

    # /sign_in
    path('sign_in', views.user_signin, name='user_signin'),

    # /sign_in
    path('sign_in_redirect', views.user_signin_redirect, name='user_signin_redirect'),

    # /sign_out
    path('sign_out', views.user_signout, name='user_signout'),

    # /user_create - not a direct url
    path('user_create', views.user_create, name='user_create'),

    # /user_profile/{{id}} - not a direct url
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),

    # /all_payment_sources/
    path('all_payment_source', views.all_payment_sources, name='all_payment_sources'),

    # /all_user_payment_sources/
    path('all_user_payment_source/<int:user_id>', views.all_user_payment_sources,
         name='all_user_payment_source'),

    # /payment_sources/{{id}}/
    path('payment_source/<int:ps_id>', views.payment_source_detail,
         name='payment_source_detail'),

    # /payment_source/new
    path('payment_source/new', views.payment_source_new,
         name='payment_source_new'),

    # /payment_sources/create
    path('payment_source/create', views.payment_source_create,
         name='payment_source_create'),

    # /transaction/new_select_source
    path('transaction/new_select_source', views.transaction_new_select_source,
         name='transaction_new_select_source'),

    # /transaction/new/pmnt_src_id={{id}}
    path('transaction/new+pmnt_src_id=<int:payment_source_id>', views.transaction_new,
         name='transaction_new'),

    # /transaction/create
    path('transaction/create', views.transaction_create, name='transaction_create'),

    # /transaction/{{id}}/
    path('transaction/<int:transaction_id>', views.transaction_detail,
         name='transaction_detail'),

    # /all_transactions/
    path('all_transactions', views.all_transactions, name='all_transactions'),

    # /all_user_transactions/
    path('all_user_transactions/<int:user_id>', views.all_user_transactions,
         name='all_user_transactions'),
]
