from django.contrib.auth.models import User
from django.db import models
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Имя')
#
#     def __str__(self):
#         return f'{self.user}'


class Ads(models.Model):
    title = models.CharField(max_length=100, default='Без названия', verbose_name='Заголовок')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # content = models.CharField(max_length=2500, default='default content', verbose_name='Контент')
    # content = HTMLField(max_length=20000, default=False, verbose_name='Контент')
    # content = RichTextField()
    content = RichTextUploadingField(null=True, config_name='default')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категории')

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField(max_length=50, default=False, verbose_name='Заголовок')

    def __str__(self):
        return f'{self.name}'


class Response(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика')

    accept_status = models.BooleanField(default = False, verbose_name='Отклик принят')
    text = models.CharField(max_length=2000, default='Текст отклика', verbose_name='Отклик')

