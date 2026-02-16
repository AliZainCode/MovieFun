import json
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import TVSeries


class TVSeriesForm(forms.ModelForm):
    class Meta:
        model = TVSeries
        fields = "__all__"
        widgets = {
            "cast_details": forms.Textarea(
                attrs={"rows": 20, "style": "font-family: monospace; width: 100%;"}
            ),
            "season_details": forms.Textarea(
                attrs={"rows": 10, "style": "font-family: monospace; width: 100%;"}
            ),
        }

@admin.register(TVSeries)
class TVSeriesAdmin(admin.ModelAdmin):
    form = TVSeriesForm

    list_display = (
        "title",
        "genre",
    )

    search_fields = ("title", "genre", "subject_id")
    list_filter = ("genre", "country", "created_at")

    readonly_fields = (
        "display_total_seasons",
        "display_total_episodes",
        "display_total_cast",
        "season_details_pretty",
        "cast_details_pretty",
        "created_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "genre", "release_date", "country", "description")
        }),
        ("IMDb Info", {"fields": ("imdb_rating", "imdb_votes")}),
        ("Series Info", {
            "fields": (
                "display_total_seasons",
                "display_total_episodes",
                "display_total_cast",
                "season_details_pretty",
            )
        }),
        ("Media & Links", {"fields": ("trailer_url", "cover_image", "play_url", "detail_path", "subject_id")}),
        ("Cast JSON (Editable)", {"fields": ("cast_details",)}),
        ("Cast Preview (Formatted)", {"fields": ("cast_details_pretty",)}),
    )


    def display_total_seasons(self, obj):
        return len(obj.season_details) if obj.season_details else 0
    display_total_seasons.short_description = "Total Seasons"


    def display_total_episodes(self, obj):
        if not obj.season_details:
            return 0
        return sum(season.get("total_episodes", 0) for season in obj.season_details)
    display_total_episodes.short_description = "Total Episodes"


    def display_total_cast(self, obj):
        return len(obj.cast_details) if obj.cast_details else 0
    display_total_cast.short_description = "Total Cast"


    def season_details_pretty(self, obj):
        if not obj.season_details:
            return "No Season Data"
        lines = [f"Season {s.get('season_number')}: {s.get('total_episodes')} episodes"
                 for s in obj.season_details]
        return format_html("<pre>{}</pre>", "\n".join(lines))
    season_details_pretty.short_description = "Season Details"


    def cast_details_pretty(self, obj):
        if not obj.cast_details:
            return "No Cast Data"
        try:
            formatted = json.dumps(obj.cast_details, indent=4)
            return format_html("<pre>{}</pre>", formatted)
        except Exception:
            return "Invalid JSON"
    cast_details_pretty.short_description = "Formatted Cast JSON"
