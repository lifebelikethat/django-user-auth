from django import forms
from django.contrib.auth import get_user_model
user_model = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
            max_length=48,
            widget=forms.TextInput(attrs={
                "placeholder": "Username",
                "autofocus": True,
                }))
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={
                "placeholder": "Password",
                }))


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
            required=True,
            widget=forms.TextInput(attrs={
                "autofocus": True,
                })
            )
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = user_model
        fields = ("email", "username", "password")


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=48)


class ChangePasswordForm(forms.Form):
    password0 = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["password0"].label = "Current Password"
        self.fields["password1"].label = "New Password"
        self.fields["password2"].label = "Confirm Password"


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["password1"].label = "New Password"
        self.fields["password2"].label = "Confirm Password"
