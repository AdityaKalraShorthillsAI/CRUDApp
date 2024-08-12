from django.urls import path
from api.views import PostView, UserLoginView, UserSignupView

urlpatterns = [
    path("user/login/", UserLoginView.as_view(), name="user-login"),
    path("user/signup/", UserSignupView.as_view(), name="user-signup"),
    path("post/", PostView.as_view(), name="post"),
    # path("post/<str:post_slug>/", PostView.as_view(), name="post"),
    path("posts/", PostView.as_view(), name="posts"),
]
