from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
# from .models import User, Profile
from applications.account.models import User, Profile
from django import forms


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomerUser
#         fields = ('first_name','last_name','username', 'birth_day', 'email','phone_number','city','address','image')


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone_number': 'شماره تلفن',
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','phone_number')
        labels = {
            'email': 'ایمیل',
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, label="ایمیل یا شماره تلفن")
    password = forms.CharField(max_length=50, label="رمز عبور", widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'date_of_birth', 'gender']


class OTPForm(forms.Form):
    email = forms.EmailField(label='ایمیل')

class VerifyOTPForm(forms.Form):
    otp = forms.CharField(label='رمز یک بار مصرف')

class OTPForm(forms.Form):
    email = forms.EmailField(label='ایمیل')
