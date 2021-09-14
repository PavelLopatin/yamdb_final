from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class UserRole(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=30, choices=UserRole.choices,
                            default=UserRole.USER)
    bio = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.is_superuser or self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRole.USER


class Genre(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    slug = models.SlugField(unique=True, max_length=20)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    slug = models.SlugField(unique=True, max_length=20)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(verbose_name="Название", db_index=True,
                            max_length=100)
    year = models.IntegerField(verbose_name="Год выпуска",
                               validators=[validate_year],
                               default=None)
    description = models.TextField(verbose_name="Описание")
    genre = models.ManyToManyField(Genre, verbose_name="Жанр", blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 verbose_name="Категория",
                                 blank=True,
                                 null=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews")
    text = models.TextField(verbose_name="Обзор", max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField(default=10, validators=[
                                MaxValueValidator(10, "Меньше 10"),
                                MinValueValidator(1, "Больше одного")])
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
