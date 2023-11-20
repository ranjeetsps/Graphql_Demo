from graphene import InputObjectType, String, Int, Boolean
from graphene_django import DjangoObjectType
import graphene
from graphene import relay

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from restAPI.models import UserProfile, Post, PostLike
                                                                                                    

class UserProfileNode(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = '__all__'
        interfaces = (relay.Node,)


class UsersNode(DjangoObjectType):
    class Meta:
        model = User
        fields =('id', 'first_name', 'last_name', 'username', 'password', 'email', 'user_profile')
        interfaces = (relay.Node,)
    

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"
        interfaces = (relay.Node,)


class PostLikeNode(DjangoObjectType):
    class Meta:
        model = PostLike
        fields = "__all__"
        interfaces = (relay.Node,)


