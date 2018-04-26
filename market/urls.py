from django.urls import path
from . import views

urlpatterns = [
    # /market/
    path('', views.index, name='index'),

    # /payment_sources/
    path('payment_sources', views.payment_sources, name='payment_sources'),

    # /payment_sources/{{id}}/
    path('payment_sources/<int:payment_source_id>', views.payment_source_detail,
         name='payment_source_detail'),

]
