from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):

    total_cast = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_total_cast(self, obj):
        return len(obj.cast_details or [])
