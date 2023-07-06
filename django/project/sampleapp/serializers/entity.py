from rest_framework_json_api import serializers
from sampleapp.models.entity import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'
