from django.urls import path
from django.contrib.auth.views import LogoutView, TemplateView
from .views import IndexView, login_user, input_code, register


urlpatterns = [
    path('pers_acc/', IndexView.as_view()),
    path('login/', login_user, name='login'),
    path('logout_confirm/', TemplateView.as_view(template_name='sign/logout_confirm.html'), name='logout_confirm'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', register, name='signup'),
    path('input_code/', input_code, name='input_code'),
    ]
