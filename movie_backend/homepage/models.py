from django.db import models

class homepagemodel(models.Model):
    
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=50)
    genre = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    imdb = models.CharField(max_length=10, blank=True, null=True)
    imdb_votes = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    cast = models.JSONField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    play_url = models.URLField(blank=True, null=True)
    subject_id = models.CharField(max_length=50, unique=True)
    detail_path = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
