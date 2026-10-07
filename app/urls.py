from django.urls import path
from . import views

urlpatterns = [
    path('add_card/', views.add_card, name='add_card'),
    path('dashboard_summary/', views.dashboard_summary, name='dashboard_summary'),
    path('pay/', views.pay, name='pay'),
    path('transaction_history/', views.transaction_history, name='transaction_history')
]