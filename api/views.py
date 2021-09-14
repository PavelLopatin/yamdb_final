import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, authentication_classes, action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ADMIN_EMAIL
from .filters import ModelFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (AdminPermission, GeneralPermission,
                          ReviewOwnerPermission)
from .serializers import (UserEmailSerializer, GenreSerializer,
                          ConfirmationCodeSerializer, UserSerializer,
                          CategoriesSerializer, TitleSlugSerializer,
                          TitleGeneralSerializer, ReviewsSerializer,
                          CommentsSerializer)


@api_view(["POST"])
@authentication_classes([])
def send_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    user, created = User.objects.get_or_create(email=email)

    confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)

    send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения: {confirmation_code}",
        ADMIN_EMAIL,
        [email],
        fail_silently=False
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
def get_user_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    confirmation_code = serializer.validated_data["confirmation_code"]

    user = get_object_or_404(User, email=email)
    code = str(uuid.uuid3(uuid.NAMESPACE_DNS, email))
    if code != confirmation_code:
        return Response({"confirmation_code": "Неверный код подтверждения"},
                        status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)

    return Response({f"token: {token}"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminPermission]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class GenreCategoriesMixin(viewsets.ModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(GenreCategoriesMixin):
    queryset = Genre.objects.all()
    lookup_field = "slug"
    serializer_class = GenreSerializer
    permission_classes = [GeneralPermission]

    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class CategoriesViewSet(GenreCategoriesMixin):
    queryset = Category.objects.all()
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [GeneralPermission]

    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filter_class = ModelFilter
    permission_classes = [GeneralPermission]
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return TitleSlugSerializer
        return TitleGeneralSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"),
                                   title=self.kwargs.get("title_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"),
                                   title=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, review=review)
