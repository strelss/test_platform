from django.db import models
import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    user_name = models.CharField(max_length=30, verbose_name='Имя', blank=True, null=True,)
    user_surname = models.CharField(max_length=30, verbose_name='Фамилия', blank=True, null=True, )
    avatar = models.FileField(verbose_name="Аватар", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="О себе")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

class PostQuiz(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='posts')
    text = models.CharField(max_length=800, verbose_name='Описание викторины', null=True, blank=True)

    title = models.CharField(max_length=200, verbose_name='Вопрос')

    class Meta:
        ordering = ["-datetime"]

class Answer(models.Model):
    postQuiz_id = models.ForeignKey(PostQuiz, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, verbose_name='Ответ')


