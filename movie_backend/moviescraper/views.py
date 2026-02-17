from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer
from .pagination import MoviePagination
from .filters import MovieFilter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class MovieListView(generics.ListAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = MovieFilter

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


class MovieDetailView(generics.RetrieveAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = "subject_id"
