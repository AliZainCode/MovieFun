from rest_framework import generics
from .models import TVSeries
from .serializers import TVSeriesSerializer
from .pagination import TVSeriesPagination
from .filters import TVSeriesFilter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class TVSeriesListView(generics.ListAPIView):

    queryset = TVSeries.objects.all().order_by("-created_at")
    serializer_class = TVSeriesSerializer
    pagination_class = TVSeriesPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = TVSeriesFilter

    search_fields = [
        "title",
        "description",
        "genre"
    ]

    ordering_fields = [
        "created_at",
        "imdb_rating",
        "release_date"
    ]


class TVSeriesDetailView(generics.RetrieveAPIView):

    queryset = TVSeries.objects.all()
    serializer_class = TVSeriesSerializer
    lookup_field = "subject_id"
