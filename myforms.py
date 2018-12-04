from django import forms

from django.forms import widgets
from django.core.exceptions import ValidationError
from blog import models


class RegForm(forms.Form):
    username = forms.CharField(max_length=18, min_length=2, label='用户名',
                               widget=widgets.TextInput(attrs={'class': 'form-control'}),
                               error_messages={'max_length':'太长了','min_length':'太短了','required':'必须填'}
                               )
    password = forms.CharField(max_length=18, min_length=2, label='密码',
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={'max_length': '太长了', 'min_length': '太短了', 'required': '必须填'}
                               )
    re_password = forms.CharField(max_length=18, min_length=2, label='确认密码',
                                  widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                  error_messages={'max_length': '太长了', 'min_length': '太短了', 'required': '必须填'}
                                  )
    email = forms.EmailField(label='邮箱',
                             widget=widgets.TextInput(attrs={'class': 'form-control'}),
                             error_messages={'invalid':'格式不合法', 'required': '必须填'}
                             )

    # 局部校验钩子函数
    def clean_username(self):
        name = self.cleaned_data.get('username')
        # 去数据库校验
        ret = models.UserInfo.objects.filter(username=name).first()
        if ret:
            raise ValidationError('用户名已存在')
        return name
        # if ret:
        #     self.add_error(name, ValidationError('用户名已存在'))
        # else:
        #     return name

    # 全局校验钩子函数
    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致')
