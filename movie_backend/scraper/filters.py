import django_filters
from .models import TVSeries


class TVSeriesFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr="icontains")
    genre = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="icontains")

    imdb_min = django_filters.NumberFilter(field_name="imdb_rating", lookup_expr="gte")
    imdb_max = django_filters.NumberFilter(field_name="imdb_rating", lookup_expr="lte")

    class Meta:
        model = TVSeries
        fields = ["title", "genre", "country"]
