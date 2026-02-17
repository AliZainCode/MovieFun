import django_filters
from .models import homepagemodel

class MovieFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr="icontains")
    genre = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.CharFilter(lookup_expr="iexact")
    country = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = homepagemodel
        fields = ["title", "genre", "type", "country"]
