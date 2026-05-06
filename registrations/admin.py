from django.contrib import admin
from .models import Product, Sale, Debt

# This tells Django to show these in the Admin dashboard
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Debt)