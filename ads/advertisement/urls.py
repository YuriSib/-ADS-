from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AdsCreate, AdsList, AdsDetail, AdsEdit, AdsDelete, MyAds


urlpatterns = [
   path('', AdsList.as_view()),

   path('ads/', AdsList.as_view(), name='ads_list'),
   path('ads/<int:pk>', AdsDetail.as_view(), name='a_ads'),

   path('ads/create/', AdsCreate.as_view(), name='ads_create'),
   path('ads/my_ads/', MyAds.as_view(), name='my_ads'),
   path('ads/<int:pk>/edit/', AdsEdit.as_view(), name='ads_edit'),
   path('ads/<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
