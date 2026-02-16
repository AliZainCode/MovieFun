from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Movie
from .serializers import MovieSerializer
from .movie_scraper import scrape_all_movies


class RunMovieScraperView(APIView):
    def post(self, request):
        scrape_all_movies()
        return Response({"message": "Movie scraper executed successfully"})


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()[:100]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
