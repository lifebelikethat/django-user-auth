from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from . import forms
from . import models
from django.contrib.auth import get_user_model
import secrets
user_model = get_user_model()


# Create your views here.
def LoginPage(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = authenticate(
                        request,
                        username=username,
                        password=password,
                        )
                login(request, user)
                return redirect('home')
            except:
                message = "No account found with those credentials."

    context = {
            "form": form,
            "message": message,
            }
    return render(request, 'user/loginPage.html', context)

def LogoutPage(request):
    logout(request)
    return redirect('login')

def RegisterPage(request):
    form = forms.RegisterForm()
    message = ""
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = user_model.objects.get(email=email)
                if user:
                    message = "Email already taken."
            except:
                user_object = form.save(commit=False)
                user_object.set_password(password)
                user_object.is_active = False
                user_object.save()
                message = ""

    context = {
            "form": form,
            "message": message,
            }
    return render(request, 'user/RegisterPage.html', context)

def ConfirmEmail(request, token):
    if request.method == "GET":
        userprofile = get_object_or_404(models.UserProfile, email_token=token)

        if userprofile:
            userprofile.email_token = ""
            userprofile.user.is_active = True
            userprofile.save()
            userprofile.user.save()

            return redirect('login')

def ResendConfirmEmail(request):
    form = forms.EmailForm()
    message = ""

    if request.method == "POST":
        form = forms.EmailForm(request.POST)

        if form.is_valid():
            email = request.POST.get("email")
            userprofile = get_object_or_404(models.UserProfile, email=email)

            if userprofile is not None and userprofile.email_token != "":
                send_mail(
                        "confirm email",
                        f"http://127.0.0.1:8000/user/confirm/{userprofile.email_token}/",
                        "settings.EMAIL_HOST_USER",
                        [email,],
                        fail_silently=False,
                        )
                message = "Check your inbox to confirm your email."

    context = {
            "form": form,
            "message": message,
            }

    return render(request, 'user/ResendConfirmEmail.html', context)

def ChangePassword(request):
    if str(request.user) == "AnonymousUser":
        return redirect('login')
    form = forms.ChangePasswordForm()
    message = {
            "password0": "",
            "password2": "",
            }

    if request.method == "POST":
        form = forms.ChangePasswordForm(request.POST)

        if form.is_valid():
            password0 = request.POST.get("password0")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            valid_user = request.user.check_password(password0)

            if valid_user and password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                user = authenticate(
                        request,
                        username=request.user.username,
                        password=password1
                        )
                if user is not None:
                    login(request, user)

                return redirect('home')

            elif not valid_user:
                message["password0"] = "invalid password"

            else:
                message["password2"] = "passwords must match"

    context = {
            "message": message,
            "form": form,
            }

    return render(request, 'user/ChangePassword.html', context)

def ResetPasswordEmail(request):
    form = forms.EmailForm()

    if request.method == "POST":
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            userprofile = get_object_or_404(models.UserProfile, email=email)

            if userprofile is not None:
                token = secrets.token_urlsafe(64)
                userprofile.password_token = token
                userprofile.save()

                send_mail(
                        "confirm email",
                        f"http://127.0.0.1:8000/user/reset-password/{token}/",
                        "settings.EMAIL_HOST_USER",
                        [email,],
                        fail_silently=False,
                        )
    message = "Check your inbox to confirm your email."
    context = {
            "form": form,
            "message": message,
            }

    return render(request, 'user/ResetPasswordEmail.html', context)

def ResetPassword(request, token):
    form = forms.ResetPasswordForm()
    message = ""

    if request.method == "POST":
        form = forms.ResetPasswordForm(request.POST)

        if form.is_valid():
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            try:
                userprofile = models.UserProfile.objects.get(password_token=token)

            except:
                return HttpResponse("URL expired")

            if password1 == password2 and userprofile is not None:
                userprofile.user.set_password(password1)
                userprofile.password_token = ""
                userprofile.save()
                userprofile.user.save()

                return redirect('login')

            else:
                message = "Passwords must match."

    context = {
            "form": form,
            "message": message,
            }

    return render(request, 'user/ResetPassword.html', context)

def ChangeEmail(request):
    message = ""

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = user_model.objects.get(email=email)
            return HttpResponse("email already taken")
        except:
            token = secrets.token_urlsafe(64)
            request.user.userprofile.temporary_email = email
            request.user.userprofile.email_token = token
            request.user.userprofile.save()

            send_mail(
                    "change email",
                    f"http://127.0.0.1/user/change-email/{token}/",
                    "settings.EMAIL_HOST_USER",
                    [email,],
                    fail_silently=True,
                    )

    return render(request, 'user/ChangeEmail.html', {})

def ChangeEmailConfirm(request, token):
    if request.method == "GET":
        try:
            userprofile = models.UserProfile.objects.get(email_token=token)
            userprofile.email = userprofile.temporary_email
            userprofile.user.email = userprofile.temporary_email
            userprofile.email_token = ""
            userprofile.temporary_email = ""
            userprofile.save()
            userprofile.user.save()
        except:
            return HttpResponse("URL expired")

    return HttpResponse("email changed")
