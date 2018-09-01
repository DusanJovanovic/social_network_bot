from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from lk import settings



class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError('Users must have a valid e-mail address')

        account = self.model(
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name', None),
            last_name=kwargs.get('last_name', None),
            email_verified=kwargs.get('email_verified', None),
        )

        account.set_password(password)
        account.save()

        return account


class Account(AbstractBaseUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email_verified = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Post(models.Model):

    post_id = models.AutoField(primary_key=True, unique=True)
    content = models.CharField(max_length=280)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_of_likes = models.IntegerField(default=0)


class Like(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)