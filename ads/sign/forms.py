from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form_input'}))
    # email = forms.CharField(label="email", widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    class Meta:
        model = get_user_model()
        fields = ['user', 'password']


class InputCodeForm(forms.Form):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    code = forms.CharField(label="Проверочный код", widget=forms.TextInput(attrs={'class': 'form_input'}))

    class Meta:
        model = UserCreationForm
        fields = ['username', 'password', 'code']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form_input'}))
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password2']
        labels = {
            'email': 'E-mail',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            print("Пароли не совпадают!")
            raise forms.ValidationError("Пароли не совпадают!")
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            print('Такой E-mail уже существует!')
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email
