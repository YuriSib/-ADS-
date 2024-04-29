from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
# from ads.advertisement.models import Author
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
#
#
# class PersonalClassView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/personal_acc.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(f"self.request = {self.request.user.id}")
#         # context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
#         # context['category'] = self.category
#         return context
#
#
# @login_required
# def upgrade_me(request):
#     user = request.user
#     premium_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         premium_group.user_set.add(user)
#         User.objects.create(user=user)
#     return redirect('to_many_post')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/personal_acc.html'

