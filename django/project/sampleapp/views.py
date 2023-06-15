from sampleapp.models import Entity

from rest_framework import viewsets
from rest_framework_json_api import serializers


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class GetNamedEnts(viewsets.ModelViewSet):
    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.all()

