from sampleapp.models.entity import Entity
from rest_framework import viewsets
from sampleapp.serializers.entity import EntitySerializer


class GetNamedEnts(viewsets.ModelViewSet):
    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.all()
