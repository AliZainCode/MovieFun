from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TVSeries
from .serializers import TVSeriesSerializer
from .scraper_service import scrape_all_series

class RunScraperView(APIView):
    def post(self, request):
        scrape_all_series(max_pages=1)  # adjust pages
        return Response({"message": "Scraping completed"}, status=200)

class TVSeriesListView(APIView):
    def get(self, request):
        series = TVSeries.objects.all().order_by('-created_at')
        serializer = TVSeriesSerializer(series, many=True)
        return Response(serializer.data)
