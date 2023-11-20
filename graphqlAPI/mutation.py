from graphql_auth.schema import MeQuery, UserQuery
import graphene
from graphqlAPI.nodes import UsersNode, PostNode, PostLikeNode
from graphql_jwt.decorators import login_required
from restAPI.models import UserProfile
from django.contrib.auth.models import User
from restAPI.serializers import UserSerializer, PostSerializer, PostLikeSerializer
from django.shortcuts import get_object_or_404
from restAPI.models import Post


class CreateUserWithProfileMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        bio = graphene.String(required=True)
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        pincode = graphene.String(required=True)
        address = graphene.String(required=False)
        contact = graphene.String(required=False)

    user = graphene.Field(UsersNode)

    @classmethod
    def mutate(cls, root, info, username, password, bio, city, state, pincode, address=None, contact=None):
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        # Create the user profile
        user_profile = UserProfile.objects.create(
            user=user,
            bio=bio,
            city=city,
            state=state,
            pincode=pincode,
            address=address,
            contact=contact
        )

        return CreateUserWithProfileMutation(user=user)


class UpdateUserWithProfileMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        username = graphene.String()
        bio = graphene.String()
        city = graphene.String()
        state = graphene.String()
        pincode = graphene.String()
        address = graphene.String()
        contact = graphene.String()

    user = graphene.Field(UsersNode)

    @classmethod
    @login_required
    def mutate(cls, root, info, user_id, **kwargs):
        user = User.objects.get(id=user_id)

        data = {'user_profile':{}}
        for key,value in kwargs.items():
            if key == "username":
                data[key] = value
            else:
                data['user_profile'][key] = value
        print(data)
        serializer = UserSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return UpdateUserWithProfileMutation(user=user)
        else:
            print(serializer.errors)
            return UpdateUserWithProfileMutation(user=serializer.errors)
        

class CreatePostMutation(graphene.Mutation):
    class Arguments:
        user = graphene.ID(required = True)
        title = graphene.String(required = True)
        caption = graphene.String(required = True)

    post = graphene.Field(PostNode)

    @classmethod
    @login_required
    def mutate(cls,root,info,**kwargs):
        print(kwargs)
        serializer = PostSerializer(data=kwargs)
        if serializer.is_valid():
            instance = serializer.save()
            return CreatePostMutation(post = instance)
        else:
            return CreatePostMutation(post = None)
        

class PostLikeMutation(graphene.Mutation):
    class Arguments:
        user = graphene.ID(required = True)
        post = graphene.ID(required = True)

    post_like = graphene.Field(PostLikeNode)

    @classmethod
    def mutate(cls,root,info,**kwargs):
        serializer = PostLikeSerializer(data = kwargs)
        post = get_object_or_404(Post,id = kwargs['post'])
        if serializer.is_valid():
            instance = serializer.save()
            post.likes += 1
            post.save()
            return PostLikeMutation(post_like = instance)
        else:
            return PostLikeMutation(post_like = None)
        
