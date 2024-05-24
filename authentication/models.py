from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Account(AbstractUser):
    pass
