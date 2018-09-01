from django.conf.urls import include, url
from .views import AuthRegister, CreatePost, LikePost, UnlikePost, GetUsersWithZeroLike
from .views import GetUsersByPosts, GetPostsByUser
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^auth/login/', obtain_jwt_token),
    url(r'^auth/token-refresh/', refresh_jwt_token),
    url(r'^auth/token-verify/', verify_jwt_token),
    url(r'^auth/register/$', AuthRegister.as_view()),
    url(r'^user/create_post/$', CreatePost.as_view()),
    url(r'^post/like/([0-9]+)/$', LikePost.as_view()),
    url(r'^post/unlike/([0-9]+)/$', UnlikePost.as_view()),
    url(r'^post/user/([0-9]+)/$', GetPostsByUser.as_view()),
    url(r'^user/zero_like/$', GetUsersWithZeroLike.as_view()),
    url(r'^user/number_of_posts/$', GetUsersByPosts.as_view())
]