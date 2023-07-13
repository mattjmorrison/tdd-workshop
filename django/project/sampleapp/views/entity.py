from sampleapp.models.entity import Entity
from rest_framework import viewsets
from sampleapp.serializers.entity import EntitySerializer, EntityV1Serializer


class GetNamedEnts(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.headers.get('X-Imtapps-Api-Version') == '2.0':
            return EntitySerializer
        return EntityV1Serializer

    def get_queryset(self):
        return Entity.objects.all()
