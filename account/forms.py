from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    #   类 RegistrationForm的 password和 password2两个密码属性是为了让用户确认自己所设置的密码，
    #   这里定义的属性意味着覆盖或者不使用在内部类 Meta的声明数据模型中的字段，
    #   在表单中相关字段对应此处重新定义的两个变量

    class Meta:
        model = User
        fields = ('username', 'email')  # 这个字段 其实就是 在上面写  username = xxx  email = xxx

    def clean_password2(self):  # 调用user_form.cleaned_data['password'] 这个的时候会调用这个函数
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match")
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
