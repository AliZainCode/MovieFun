from django.urls import path
from .views import RunScraperView, TVSeriesListView

urlpatterns = [
    path('run-scraper/', RunScraperView.as_view()),
    path('series/', TVSeriesListView.as_view()),
]
