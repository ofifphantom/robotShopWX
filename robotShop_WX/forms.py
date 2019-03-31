#!usr/bin/python#coding=utf-8

from django import forms
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
class RegisterForm(forms.Form):

    phoneNumber = forms.CharField(label='phoneNumber')
    identityCode = forms.CharField(label='identityCode')





