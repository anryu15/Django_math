from django.db import models

from django.contrib.auth.models import User
from sqlalchemy import null

# Create your models here.

class AccountUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    numgood = models.IntegerField('good',default=0)
    contents = models.TextField("contents", null=True) 

    def __str__(self):
        return self.user.username