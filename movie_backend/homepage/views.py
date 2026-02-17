from rest_framework import generics
from .models import homepagemodel
from .serializers import HomePageSerializer
from .pagination import MoviePagination
from .filters import MovieFilter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class HomePageListView(generics.ListAPIView):

    queryset = homepagemodel.objects.all().order_by("-created_at")
    serializer_class = HomePageSerializer
    pagination_class = MoviePagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = MovieFilter

    search_fields = [
        "title",
        "description",
        "genre"
    ]

    ordering_fields = [
        "created_at",
        "imdb",
        "release_date"
    ]


class HomePageDetailView(generics.RetrieveAPIView):

    queryset = homepagemodel.objects.all()
    serializer_class = HomePageSerializer
    lookup_field = "subject_id"
