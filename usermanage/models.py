from django.contrib.auth.models import User
from django.db import models

from django_iban.fields import IBANField


# Create your models here.


class IbanUser(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    iban = IBANField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.iban})'
