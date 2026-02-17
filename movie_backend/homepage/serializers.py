from rest_framework import serializers
from .models import homepagemodel

class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = homepagemodel
        fields = "__all__"
