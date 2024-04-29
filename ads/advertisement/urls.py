from django.urls import path
from .views import AdsCreate, AdsList, AdsDetail, AdsEdit, AdsDelete


urlpatterns = [
   path('', AdsList.as_view()),

   path('ads/', AdsList.as_view(), name='news_list'),
   path('ads/<int:pk>', AdsDetail.as_view(), name='a_ads'),

   path('ads/create/', AdsCreate.as_view(), name='ads_create'),
   path('news/<int:pk>/edit/', AdsEdit.as_view(), name='ads_edit'),
   path('news/<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete')
]