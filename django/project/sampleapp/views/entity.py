from sampleapp.models.entity import Entity
from rest_framework import viewsets
from sampleapp.serializers.entity import EntitySerializer, LegacyEntitySerializer


class GetNamedEnts(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.headers.get('X-imtapps-Api-Version', '1.0') == '1.0':
            return LegacyEntitySerializer
        if self.request.headers.get('X-Imtapps-Api-Version', '').startswith('2.'):
            return EntitySerializer

    def get_queryset(self):
        return Entity.objects.all()
