import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr="icontains")
    genre = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="icontains")

    imdb_min = django_filters.NumberFilter(field_name="imdb_rating", lookup_expr="gte")
    imdb_max = django_filters.NumberFilter(field_name="imdb_rating", lookup_expr="lte")

    is_homepage = django_filters.BooleanFilter()

    class Meta:
        model = Movie
        fields = ["genre", "country", "is_homepage"]
