import django_filters
from restAPI.models import UserProfile
from django.contrib.auth.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username','email']


class UserProfileFilter(django_filters.FilterSet):

    class Meta:
        model = UserProfile
        fields = ['bio','pincode','user']

