from rest_framework import serializers
from .models import TVSeries


class TVSeriesSerializer(serializers.ModelSerializer):

    total_seasons_count = serializers.SerializerMethodField()
    total_episodes_count = serializers.SerializerMethodField()

    class Meta:
        model = TVSeries
        fields = "__all__"

    def get_total_seasons_count(self, obj):
        return len(obj.season_details or [])

    def get_total_episodes_count(self, obj):
        if not obj.season_details:
            return 0
        return sum(s.get("total_episodes", 0) for s in obj.season_details)
