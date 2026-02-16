from django.db import models


class Movie(models.Model):
    
    title = models.CharField(max_length=500, db_index=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    imdb_rating = models.FloatField(blank=True, null=True, db_index=True)
    imdb_votes = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cast_details = models.JSONField(default=list, blank=True)
    trailer_url = models.TextField(blank=True, null=True)
    cover_image = models.TextField(blank=True, null=True)
    detail_path = models.TextField(blank=True, null=True)
    subject_id = models.TextField(unique=True)
    play_url = models.TextField(blank=True, null=True)
    is_homepage = models.BooleanField(default=False, db_index=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title
