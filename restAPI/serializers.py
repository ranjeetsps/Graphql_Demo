from django.contrib.auth.models import User
from rest_framework import serializers
from restAPI.models import UserProfile, Post, PostLike, UserFollower

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'city','state','pincode','address']

class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('user_profile', None)
        user = super(UserSerializer, self).create(validated_data)

        password = validated_data.get('password')
        user.set_password(password)
        user.save()

        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)

        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user_profile', None)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()

        if profile_data:
            user_profile = instance.user_profile
            user_profile.bio = profile_data.get('bio', user_profile.bio)
            user_profile.city = profile_data.get('city', user_profile.city)
            user_profile.state = profile_data.get('state', user_profile.state)
            user_profile.pincode = profile_data.get('pincode', user_profile.pincode)
            user_profile.address = profile_data.get('address', user_profile.address)
            user_profile.save()

        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'