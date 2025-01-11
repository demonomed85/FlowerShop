from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Логин',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Пароль',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Повторите пароль',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Имя',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='Фамилия'
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    phone_number = forms.CharField(
        required=True,
        label='Номер телефона'
    )
    address = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label='Адрес'
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('Логин может содержать только латинские буквы и цифры.')

        # Проверка на уникальность имени пользователя
        if User.objects.filter(username=username).exists():
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Пароль должен содержать не менее 8 символов, включая хотя бы один спецсимвол.')
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Пароли не совпадают.')
        return confirm_password

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 3 or not re.match(r'^[a-zA-Zа-яА-ЯёЁ]+$', first_name):  # Добавлено поддержка русских букв
            raise ValidationError('Имя должно содержать не менее 3 букв и не должно содержать спецсимволы.')
        return first_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email):
            raise ValidationError('Введите корректный адрес электронной почты.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = re.compile(r'^(?:\+7|8)?(?:\s?\d{3})?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$')
        if not pattern.match(phone_number):
            raise ValidationError('Введите корректный номер телефона.')
        return phone_number