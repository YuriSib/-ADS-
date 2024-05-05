from django.contrib.auth.models import User
from django.db import models


class OneTimeCode(models.Model):
    code = models.CharField(max_length=10, verbose_name='Проверочный код')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='one_time_codes', unique=True)
    status = models.BooleanField(default=False, verbose_name='Код введен')
