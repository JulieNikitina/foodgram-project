from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(verbose_name='Имя', max_length=20, blank=True)
    first_name = None
    last_name = None
    email = models.EmailField(verbose_name='Адрес электронной\nпочты', unique=True)