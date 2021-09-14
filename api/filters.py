from django_filters import ModelChoiceFilter, FilterSet, CharFilter

from .models import Category, Genre, Title


class ModelFilter(FilterSet):
    genre = ModelChoiceFilter(field_name="genre__slug",
                              to_field_name="slug",
                              queryset=Genre.objects.all())
    category = ModelChoiceFilter(field_name="category__slug",
                                 to_field_name="slug",
                                 queryset=Category.objects.all())
    name = CharFilter(field_name="name",
                      lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ("genre", "category", "year", "name")
