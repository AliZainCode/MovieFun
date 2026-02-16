from django.db import models

class TVSeries(models.Model):

    title = models.CharField(max_length=500)  
    genre = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    imdb_rating = models.FloatField(blank=True, null=True)
    imdb_votes = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True) 

    total_seasons = models.IntegerField(default=0)
    total_episodes = models.IntegerField(default=0)

    season_details = models.JSONField(default=list, blank=True)
    cast_details = models.JSONField(default=list, blank=True)

    trailer_url = models.TextField(blank=True, null=True)  
    cover_image = models.TextField(blank=True, null=True)  

    detail_path = models.TextField(blank=True, null=True)  
    subject_id = models.TextField(unique=True)  
    play_url = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

