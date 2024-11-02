from django.db import models
from django.contrib.auth.models import AbstractUser


class PostBody(models.Model):
    heading = models.CharField(max_length=50)
    text = models.TextField()
    status = models.CharField(max_length=255, default="published")
    published_on = models.DateField(null=True, blank=True)


class User(models.Model):
    ms_number = models.CharField(max_length=4, primary_key=True)
    is_admin = models.BooleanField()


class Post(models.Model):
    fk_ms_number = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_body_id = models.ForeignKey(PostBody, on_delete=models.CASCADE)
    upvotes = models.IntegerField(null=True, blank=True)
    downvotes = models.IntegerField(null=True, blank=True)
    is_anonym = models.BooleanField()


class Comment(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


class ChangedBy(models.Model):
    pk_fk_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    pk_fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_body_id = models.ForeignKey(PostBody, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("pk_fk_post_id", "pk_fk_user_id"),)
