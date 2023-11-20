from django.urls import path
from restAPI.views import *


urlpatterns = [
    path("signup",SignUpView.as_view(),name="signUp"),
    path("signin",SignInView.as_view(),name="signIn"),
    path('users',ListUsersView.as_view(),name="list_users"),
    path('user/<int:user_id>',UserProfileView.as_view(),name="get_user"),
    path('user/<int:user_id>/update',UserProfileView.as_view(),name="update_user"),
    path('user/<int:user_id>/post',CreatePostView.as_view(),name='create_post'),
    path('user/<int:user_id>/post/<int:post_id>',LikePostView.as_view(),name="like_post"),
    path("posts",ListPostsView.as_view(),name="list_posts"),

]