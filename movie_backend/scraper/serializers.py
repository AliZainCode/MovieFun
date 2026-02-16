from rest_framework import serializers
from .models import TVSeries

class TVSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVSeries
        fields = '__all__'
