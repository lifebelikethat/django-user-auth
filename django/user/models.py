from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
import secrets
user_model = get_user_model()


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
            )
    slug = models.SlugField()
    display_name = models.CharField(
            max_length=48,
            )
    username = models.CharField(
            max_length=48,
            blank=True,
            )
    email = models.EmailField(
            max_length=48,
            blank=True,
            )
    temporary_email = models.EmailField(
            max_length=48,
            blank=True,
            )
    email_token = models.CharField(
            max_length=128,
            blank=True,
            )
    password_token = models.CharField(
            max_length=128,
            blank=True,
            )

    def __str__(self):
        return self.username

def create_user_post(sender, instance, **kwargs):
    token = secrets.token_urlsafe(64)

    try:
        userprofile = user_model.objects.get(username=instance.username).userprofile
        if userprofile:
            return None
    except:
        userprofile = UserProfile.objects.create(
                user=instance,
                username=instance.username,
                email=instance.email,
                email_token=token,
                )

        send_mail(
                "confirm email",
                f"http://127.0.0.1:8000/user/confirm/{token}/",
                "settings.EMAIL_HOST_USER",
                [instance.email],
                fail_silently=False,
                )

        userprofile.save()

post_save.connect(create_user_post, sender=user_model)
