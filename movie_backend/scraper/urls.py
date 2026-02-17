from django.urls import path
from .views import TVSeriesListView, TVSeriesDetailView

urlpatterns = [
    path("", TVSeriesListView.as_view()),
    path("series/<str:subject_id>/", TVSeriesDetailView.as_view()),
]
