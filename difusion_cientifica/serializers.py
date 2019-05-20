from rest_framework import serializers
from difusion_cientifica.models import EventoDifusion


class EventoDifusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoDifusion
        fields = '__all__'