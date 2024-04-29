from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Имя')
#
#     def __str__(self):
#         return f'{self.user}'


class Ads(models.Model):
    title = models.CharField(max_length=100, default='Без названия', verbose_name='Заголовок')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # content = models.CharField(max_length=2500, default='default content', verbose_name='Контент')
    content = HTMLField(max_length=2500, default=False, verbose_name='Контент')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категории')

    def __str__(self):
        return f'{self.title}: {self.content[:50]}'


class Category(models.Model):
    name = models.CharField(max_length=50, default=False, verbose_name='Заголовок')

    def __str__(self):
        return f'{self.name}'


class Response(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name='Автор')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика')

