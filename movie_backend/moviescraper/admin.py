import json
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
        widgets = {
            "cast_details": forms.Textarea(
                attrs={
                    "rows": 20,
                    "style": "font-family: monospace; width: 100%;"
                }
            ),
        }



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieForm

    list_display = (
        "title",
        "genre",
    )

    search_fields = ("title", "genre", "subject_id")
    list_filter = ("genre", "country", "created_at")
    ordering = ("-created_at",)

    readonly_fields = (
        "display_total_cast",
        "cast_details_pretty",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        
        ("Basic Info", {
            "fields": (
                "title",
                "genre",
                "release_date",
                "country",
                "description",
            )
        }),

        ("IMDb Info", {
            "fields": (
                "imdb_rating",
                "imdb_votes",
            )
        }),

        ("Cast Info", {
            "fields": (
                "display_total_cast",
                "cast_details",
            )
        }),

        ("Cast Preview (Formatted)", {
            "fields": (
                "cast_details_pretty",
            )
        }),

        ("Media & Links", {
            "fields": (
                "trailer_url",
                "cover_image",
                "play_url",
                "detail_path",
                "subject_id",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


    def display_total_cast(self, obj):
        return len(obj.cast_details) if obj.cast_details else 0
    display_total_cast.short_description = "Total Cast"

    def cast_details_pretty(self, obj):
        if not obj.cast_details:
            return "No Cast Data"
        try:
            formatted = json.dumps(obj.cast_details, indent=4)
            return format_html("<pre>{}</pre>", formatted)
        except Exception:
            return "Invalid JSON"
    cast_details_pretty.short_description = "Formatted Cast JSON"
