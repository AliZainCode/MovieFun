from django.urls import path
from .views import HomePageListView, HomePageDetailView

urlpatterns = [
    path("", HomePageListView.as_view()),
    path("details/<str:subject_id>/", HomePageDetailView.as_view()),
]
