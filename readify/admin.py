from django.contrib import admin
from readify.models import Book, Category, Address, Order, Cart

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Cart)


