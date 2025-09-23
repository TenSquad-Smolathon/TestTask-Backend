from rest_framework import serializers
from .models import Evacuation

class EvacuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evacuation
        fields = '__all__'