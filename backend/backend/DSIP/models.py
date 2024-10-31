from django.db import models
from django.contrib.auth.models import AbstractUser
from torch.nn.functional import selu_


class Site(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="site/logo")

    def __str__(self):
        return self.name


class User(models.Model):
    number = models.CharField(max_length=4)
    user_name = models.CharField(max_length=100)
    avatar = models.ImageField(
        upload_to="users/avatars/%Y%m%d/", default="users/avatars/default.jpg"
    )
