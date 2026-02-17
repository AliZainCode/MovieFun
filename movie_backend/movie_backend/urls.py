from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/homepage/', include('homepage.urls')),
    path('api/tvseries/', include('scraper.urls')),
    path('api/movies/', include('moviescraper.urls')),
]
