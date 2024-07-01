from django.contrib.auth.forms import AuthenticationForm
from django import forms

from users.models import User


class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField()
    password = forms.CharField()

    # username = forms.CharField(
    #     label = 'Логин:',
    #     widget=forms.TextInput(attrs={"autofocus": True,
    #                            "class": "form-control",
    #                            "placeholder": "Введите ваш логин"})
    # )
    # password = forms.CharField(
    #     label = 'Пароль:',
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                     "class": "form-control",
    #                                     "placeholder": "Введите ваш пароль"})
    # )

    class Meta:
        model = User
        fields = ["username", "password"]