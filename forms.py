from django import forms
from .models import *

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uphone','upwd']
        labels = {
            'uphone':'手机号',
            'upwd':'密码',
        }
        widgets = {
            'uphone':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'name':'uname',
                }
            ),
            'upwd':forms.PasswordInput(
                attrs={
                    'name':'upwd',
                    'class': 'form-control',
                    'placeholder':'请输入密码'
                }
            )
        }
