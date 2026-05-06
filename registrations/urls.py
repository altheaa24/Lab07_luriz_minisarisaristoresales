from django.urls import path
from .views import process_sale, record_debt, list_products

urlpatterns = [
    path('products/', list_products, name='list_products'),
    path('sales/', process_sale, name='process_sale'),
    path('debts/', record_debt, name='record_debt'),
]