from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    author = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    price = models.FloatField()
    rate = models.FloatField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='book', null=True, blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    nearby = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city} - {self.town}'


# class Purchase(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase')
#     book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='purchase')
#     is_purchased = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.user} purchased {self.book}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    book = models.ManyToManyField('Book', related_name='order')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='order')
    extra_info = models.TextField(null=True, blank=True)
    # is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f'order to {self.user.first_name} {self.user.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# class City(models.Model):
#     name = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='cart')
    quantity = models.IntegerField(default=1)
    # total_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.book}'



