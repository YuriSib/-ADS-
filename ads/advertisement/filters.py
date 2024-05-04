from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Response
from django import forms
from django.contrib.auth.models import User
from django.db.models.query import QuerySet



class ResponseFilter(FilterSet):

    class Meta:
        model = Response
        fields = {
            'ads': ['exact'],
        }