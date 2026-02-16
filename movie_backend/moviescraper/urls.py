from django.urls import path
from .views import RunMovieScraperView, MovieListView

urlpatterns = [
 
    path('run-scraper/', RunMovieScraperView.as_view(), name='run_movie_scraper'),

    path('', MovieListView.as_view(), name='movie_list'),
]
