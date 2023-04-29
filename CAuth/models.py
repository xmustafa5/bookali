from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class EmailAccountManager(UserManager):

    def GET_BY_NATURAL_KEY(self, username):
        case_insensitive_username_field = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not email:
            raise ValueError('user should have an email')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.is_active = False
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class EmailAccount(AbstractUser):
    username = models.NOT_PROVIDED
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('Email Address', unique=True)
    phone_number = models.CharField(max_length=14)
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=4, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmailAccountManager()

    def __str__(self):
        return self.email

