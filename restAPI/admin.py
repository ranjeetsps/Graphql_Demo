from django.contrib import admin
from restAPI.models import UserFollower, UserProfile, Post, PostLike


admin.site.register(UserFollower)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(PostLike)