from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class ProfileInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birthday = forms.DateField()
