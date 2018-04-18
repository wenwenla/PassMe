from django import forms
from django.contrib.auth.models import User

from Ticks.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '请输入用户名'
                               }))
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '请输入密码'
                               }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入邮箱'
    }))

    partner = forms.CharField(max_length=30, required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': '请输入伙伴邀请码'
                              }))

    introduce = forms.CharField(max_length=128, required=False, empty_value='这个人太懒了，什么都没有留下',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': '自我介绍??',
                                }))

    code = forms.CharField(max_length=128,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': '请输入来自wenwenla的邀请码'
                           }))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '请输入用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '请输入密码'}))
