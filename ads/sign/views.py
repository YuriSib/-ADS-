import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail

from .forms import LoginUserForm, InputCodeForm, RegisterUserForm
from .models import OneTimeCode
from .passwords import login  as email


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/personal_acc.html'


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            print(request)
            print(cd['username'], cd['password'])
            if not OneTimeCode.objects.filter(user__username=cd['username']):
                print('В модели нет такого объекта')
                return HttpResponse('В модели нет такого объекта, пройдите регистрацию!')
                # return render(request, 'sign/login.html', {'form': form})
            else:
                if OneTimeCode.objects.get(user__username=cd['username']).status:
                    # Успешно входим
                    login(request, user)
                    return HttpResponseRedirect(reverse('ads_list'))
                else:
                    # Введем проверочный код
                    return HttpResponseRedirect(reverse('input_code'))
    else:
        form = LoginUserForm()
    return render(request, 'sign/login.html', {'form': form})


def register(request):
    print(request)
    if request.method == "POST":
        print(request)
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            letters = string.ascii_letters
            code = ''.join(random.choice(letters) for _ in range(6))
            OneTimeCode.objects.create(code=code, user=user)

            user_email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            send_mail(
                subject=f'{username}',
                message=f'''Ваш проверочный код: {code} для завершения регистрации.''',
                from_email=f'''{email}@yandex.ru''',
                recipient_list=[user_email]
            )

            return HttpResponseRedirect(reverse('input_code'))

    form = RegisterUserForm()
    return render(request, 'sign/signup.html', {'form': form})


def input_code(request):
    print('input_code')
    print(request)
    if request.method == 'POST':
        print('POST')
        form = InputCodeForm(request.POST)
        if form.is_valid():
            print('form is valid')
            cd = form.cleaned_data
            input_cod = cd['code']
            username = cd['username']
            print(username)
            user_id = User.objects.get(username=username).id
            print(f'user_id = {user_id}, начинаю проверку условия')

            if input_cod == OneTimeCode.objects.get(user=user_id).code:
                print(input_cod, 'is True')
                code_object = OneTimeCode.objects.get(user=user_id)
                code_object.status = 1
                code_object.save(update_fields=['status'])

                print(username, cd['password'])
                user = authenticate(request, username=username, password=cd['password'])
                print(type(user))
                login(request, user)

                return HttpResponseRedirect(reverse('ads_list'))
            else:
                return HttpResponse('Код введен неправильно, попробуйте заново!')
        else:
            print('form is not valid')
            render(request, 'advertisement/ads_list.html')
    else:
        print('not POST')
        form = InputCodeForm()
        return render(request, 'sign/input_code.html', {'form': form})
