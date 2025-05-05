from django.db import models
from django.contrib.auth.models import AbstractUser
import os

from rest_framework.exceptions import ValidationError


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.username}.{ext}"
    return os.path.join('avatars', filename)

class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts/")
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - ის პოსტი'



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


    class Meta:
        unique_together = ('user', 'post')



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -მა დადო პოსტი- {str(self.post)}'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -მა დადო პოსტი- {str(self.post)}'

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.follower == self.following:
            raise ValidationError("მომხმარებელს არ შეუძლია საკუთარი თავის აფოლოვება.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.follower.username} აფოლოვებს {self.following.username}'

    class Meta:
        unique_together = ('follower', 'following')
