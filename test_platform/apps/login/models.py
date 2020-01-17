from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    user_name = models.CharField(max_length=30, verbose_name='Имя', blank=True, null=True,)
    user_surname = models.CharField(max_length=30, verbose_name='Фамилия', blank=True, null=True, )
    avatar = models.FileField(verbose_name="Аватар", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="О себе")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
