from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from restAPI.serializers import UserSerializer, PostLikeSerializer, PostSerializer, ListPostSerializer
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from restAPI.pagination import ListUsersPagination, ListPostsPagination
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from restAPI.models import Post, PostLike


class SignUpView(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors':str(e)})


class SignInView(APIView):

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            print(username,password)

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }

                return Response({'tokens': tokens}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e :
            return Response({'errors':str(e)})
        

class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ListUsersPagination

    def get(self, request):
        try:
            queryset = User.objects.all()
            paginator = ListUsersPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            serializer = UserSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)})

    def put(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)})


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,user_id):
        try:
            data = request.data.copy()
            data['user'] = user_id
            serializer = PostSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, user_id):
        try:
            post = get_object_or_404(Post, id=post_id)

            like_serializer = PostLikeSerializer(data={'user':user_id , 'post':post_id })
            
            if like_serializer.is_valid():
                like_serializer.save()
                post.likes += 1
                post.save()

                return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
            
            return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListPostsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ListPostsPagination

    def get(self, request):
        try:
            queryset = Post.objects.all()
            paginator = ListPostsPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            serializer = ListPostSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
