from django.contrib import admin
from .models import homepagemodel
import json

@admin.register(homepagemodel)
class HomePageModelAdmin(admin.ModelAdmin):
    list_display = ("title",  "genre", )
    search_fields = ("title", "genre", "country", "subject_id")
    list_filter = ("title", "type", "genre")

   
    readonly_fields = (
        "title",
        "type",
        "genre",
        "release_date",
        "country",
        "description",
        "imdb",
        "imdb_votes",
        "duration",
        "cast_pretty", 
        "trailer_url",
        "cover_image",
        "play_url",
        "subject_id",
        "detail_path",
        "created_at",
    )


    def cast_pretty(self, obj):
        try:
            return "{}".format(json.dumps(obj.cast, indent=2, ensure_ascii=False))
        except:
            return obj.cast
    cast_pretty.allow_tags = True  
    cast_pretty.short_description = "Cast Details"

    fieldsets = (
        (None, {
            "fields": (
                "title",
                "type",
                "genre",
                "release_date",
                "country",
                "description",
                "imdb",
                "imdb_votes",
                "duration",
                "cast_pretty", 
                "trailer_url",
                "cover_image",
                "play_url",
                "subject_id",
                "detail_path",
                "created_at",
            )
        }),
    )
