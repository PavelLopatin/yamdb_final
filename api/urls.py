from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (send_confirmation_code, get_user_token,
                    UserViewSet, CategoriesViewSet, GenreViewSet,
                    TitleViewSet, CommentViewSet, ReviewViewSet)

v1_router = DefaultRouter()

reviews_url = r"titles/(?P<title_id>\d+)/reviews"
comments_url = reviews_url + r"/(?P<review_id>\d+)/comments"

v1_router.register("users", UserViewSet)
v1_router.register("categories", CategoriesViewSet)
v1_router.register("genres", GenreViewSet)
v1_router.register("titles", TitleViewSet, basename="titles")
v1_router.register(reviews_url, ReviewViewSet, basename="review")
v1_router.register(comments_url, CommentViewSet, basename="comments")


urlpatterns = [
    path("v1/auth/email", send_confirmation_code),
    path("v1/auth/token", get_user_token),
    path("v1/", include(v1_router.urls)),
]
