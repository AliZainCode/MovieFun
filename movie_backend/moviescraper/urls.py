from django.urls import path
from .views import MovieListView, MovieDetailView

urlpatterns = [
    path("", MovieListView.as_view()),
    path("movies/<str:subject_id>/", MovieDetailView.as_view()),
]
