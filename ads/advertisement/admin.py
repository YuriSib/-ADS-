from django.contrib import admin
from .models import Ads, News
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdsAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Ads
        fields = '__all__'


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    save_on_top = True
    save_as = True
    form = AdsAdminForm


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", )
    save_on_top = True
    save_as = True
    form = AdsAdminForm


# admin.site.register(Ads)

