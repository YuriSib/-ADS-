from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Response
from django import forms
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Response
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по id автора (нужно переделать на фильтрацию по username)
            'ads': ['exact'],
        }