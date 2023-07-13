from rest_framework_json_api import serializers
from sampleapp.models.entity import Entity
from sampleapp.serializers.segment import SegmentSerializer


class LegacyEntitySerializer(serializers.ModelSerializer):
    output = serializers.SerializerMethodField()

    def get_output(self, obj):
        output = []
        for seg in obj.segment_set.all():
            output.append({'ent': seg.ent, 'label': seg.label})
        return output

    class Meta:
        model = Entity
        fields = ('sentence', 'output')


class EntitySerializer(serializers.ModelSerializer):
    included_serializers = {
        'segments': SegmentSerializer
    }

    class Meta:
        model = Entity
        exclude = ('legacy_output', )
