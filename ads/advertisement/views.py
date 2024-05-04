import datetime
from datetime import date
import logging

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.mail import send_mail

from .models import Ads, Category, Response
from .filters import ResponseFilter
from .forms import AdsForm, ResponseForm
from sign.passwords import host_password, login


class AdsList(ListView):
    model = Ads
    ordering = 'time_create'

    # queryset = Post.objects.order_by('time_create')

    template_name = 'advertisement/ads_list.html'
    context_object_name = 'Ads'
    paginate_by = 5

    def get_queryset(self):
        # self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Ads.objects.order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        # context['category'] = self.category

        return context


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    ordering = 'user'

    template_name = 'advertisement/response_list.html'
    context_object_name = 'Responses'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        ads_queryset = Ads.objects.filter(author_id=self.request.user.id)
        # queryset = Response.objects.none()
        for ads in ads_queryset:
            queryset.union(Response.objects.filter(ads_id=ads.id))

        self.filterset = ResponseFilter(self.request.GET, queryset)
        print(type(queryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class AdsDetail(DetailView):
    model = Ads
    template_name = 'advertisement/a_ads.html'
    context_object_name = 'A_ads'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(queryset=self.queryset)
        return obj


class AdsCreate(LoginRequiredMixin, CreateView):
    form_class = AdsForm
    model = Ads
    template_name = 'advertisement/ads_edit.html'
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        ads = form.save(commit=False)
        print(f'Запрос: {self.request.user.id}')
        ads.author = self.request.user

        author_id = self.request.user.id
        date_create = date.today()
        date_list = [dt.strftime("%Y-%m-%d") for dt in Ads.objects.filter(author=author_id).values_list('time_create',
                                                                                                        flat=True)]
        print(f'ads = {ads}, user_id = {author_id}, date_create = {date_create}, date_list = {date_list}')
        if date_list.count(date_create) <= 15:
            print(f'Публикаций пользователя {self.request.user} за сегодня - {date_list.count(date_create)} шт.')
            ads.save()
            print('Пост сохранен')
            return redirect('/ads/')
        else:
            print('Пост не сохранен')
            print(self.get_context_data(form=form))


class LeaveResponse(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'advertisement/response.html'
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        response = form.save(commit=False)

        response.user = self.request.user
        ads_id = int(self.request.path.replace('/ads/', '').replace('/response', ''))
        response.ads = Ads.objects.get(pk=ads_id)

        response.save()

        # user_email = User.objects.get(pk=self.request.user).email
        # send_mail(
        #     subject=f'{response.user} {response.date.strftime("%Y-%M-%d")}',
        #     message=response.ads,
        #     from_email=f'{login}@yandex.ru',
        #     recipient_list=[user_email]
        # )
        return redirect('/ads/')


class AdsEdit(LoginRequiredMixin, UpdateView):
    permission_required = ('ads.change_ads',)
    form_class = AdsForm
    model = Ads
    template_name = 'advertisement/ads_edit.html'
    success_url = reverse_lazy('ads_list')


class AdsDelete(LoginRequiredMixin, DeleteView):
    model = Ads
    template_name = 'advertisement/ads_delete.html'
    success_url = reverse_lazy('ads_list')


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'advertisement/delete_response.html'
    success_url = reverse_lazy('my_ads')


class MyAds(LoginRequiredMixin, ListView):
    model = Ads
    ordering = 'time_create'

    template_name = 'advertisement/pers_ads.html'
    context_object_name = 'My_ads'
    paginate_by = 5

    def get_queryset(self):
        queryset = Ads.objects.filter(author_id=self.request.user.id)
        print(f"queryset - {queryset}")
        return queryset


class AdsResponse(LoginRequiredMixin, ListView):
    model = Response
    ordering = 'time_create'

    template_name = 'advertisement/pers_response.html'
    context_object_name = 'My_response'
    paginate_by = 10

    def get_queryset(self):
        ads_id = self.request.path[-1]
        queryset = Response.objects.filter(ads=ads_id)
        return queryset



