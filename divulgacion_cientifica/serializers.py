from rest_framework import serializers
from . models import EventoDivulgacion


class EventoDivulgacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoDivulgacion
        fields = '__all__'