from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    city = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=255, blank=False)
    pincode = models.CharField(max_length=10, blank=False)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=15, blank=True)
    followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_post")
    title = models.CharField(max_length=255,blank=False)
    caption = models.CharField(max_length=250,blank=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


class UserFollower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'